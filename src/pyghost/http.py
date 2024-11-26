"""
Base HTTP client implementation for the Ghost Security API.
"""
import os
import logging
from typing import Any, Optional, Dict
import asyncio
import requests
import aiohttp
from aiohttp.client_exceptions import ClientError
from dotenv import load_dotenv

from .config import GhostConfig
from .exceptions import (
    GhostAPIError,
    ClientNotInitializedError,
    ConnectionError,
    RetryError
)

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

# Constants from environment
MAX_RETRIES = int(os.getenv("GHOST_MAX_RETRIES", "3"))
RETRY_DELAY = int(os.getenv("GHOST_RETRY_DELAY", "1"))  # seconds
REQUEST_TIMEOUT = int(os.getenv("GHOST_REQUEST_TIMEOUT", "30"))  # seconds


class BaseHttpClient:
    """Base class for HTTP operations."""
    
    def __init__(self, api_key: str, base_url: Optional[str] = None):
        """Initialize the HTTP client."""
        if not api_key:
            raise ValueError("API key is required")
        self.config = GhostConfig(api_key=api_key, base_url=base_url)


class SyncHttpClient(BaseHttpClient):
    """Synchronous HTTP client implementation."""
    
    def __init__(self, api_key: str, base_url: Optional[str] = None):
        """Initialize the synchronous client."""
        super().__init__(api_key, base_url)
        self.session = requests.Session()

    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
        **kwargs
    ) -> Any:
        """Make a synchronous request to the Ghost Security API."""
        url = self.config.get_api_url(endpoint)
        logger.debug(f"Making {method} request to {url}")
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                headers=self.config.headers,
                params=params,
                json=data,
                timeout=REQUEST_TIMEOUT,
                **kwargs
            )
            
            response.raise_for_status()
            
            if response.content:
                return response.json()
            return None
            
        except requests.exceptions.HTTPError as e:
            error_msg = str(e)
            error_response = None
            
            try:
                error_response = e.response.json()
                error_msg = error_response.get('message', str(e))
            except (ValueError, AttributeError):
                pass
                
            raise GhostAPIError(
                message=error_msg,
                status_code=e.response.status_code if e.response else None,
                response=error_response
            )
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Request failed: {str(e)}")


class AsyncHttpClient(BaseHttpClient):
    """Asynchronous HTTP client implementation."""
    
    def __init__(self, api_key: str, base_url: Optional[str] = None):
        """Initialize the asynchronous client."""
        super().__init__(api_key, base_url)
        self._session = None
        self._retry_count = 0

    async def __aenter__(self):
        """Async context manager entry."""
        timeout = aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)
        self._session = aiohttp.ClientSession(timeout=timeout)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self._session:
            await self._session.close()
            self._session = None
            self._retry_count = 0

    async def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
        **kwargs
    ) -> Any:
        """
        Make an asynchronous request to the Ghost Security API with retry logic.
        
        Args:
            method: HTTP method
            endpoint: API endpoint
            params: Query parameters
            data: Request body
            **kwargs: Additional arguments for the request
            
        Returns:
            API response data
            
        Raises:
            ClientNotInitializedError: If client is not initialized
            ConnectionError: If connection fails
            RetryError: If max retries exceeded
            GhostAPIError: If API returns an error
        """
        if not self._session:
            raise ClientNotInitializedError()
            
        url = self.config.get_api_url(endpoint)
        logger.debug(f"Making async {method} request to {url}")
        
        while self._retry_count < MAX_RETRIES:
            try:
                async with self._session.request(
                    method=method,
                    url=url,
                    headers=self.config.headers,
                    params=params,
                    json=data,
                    **kwargs
                ) as response:
                    response.raise_for_status()
                    
                    if response.content_length:
                        result = await response.json()
                        self._retry_count = 0  # Reset on success
                        return result
                    return None
                    
            except aiohttp.ClientResponseError as e:
                error_msg = str(e)
                error_response = None
                
                try:
                    error_response = await response.json()
                    error_msg = error_response.get('message', str(e))
                except (ValueError, AttributeError):
                    pass
                    
                raise GhostAPIError(
                    message=error_msg,
                    status_code=e.status if hasattr(e, 'status') else None,
                    response=error_response
                )
                
            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                self._retry_count += 1
                if self._retry_count >= MAX_RETRIES:
                    raise RetryError(
                        f"Max retries ({MAX_RETRIES}) exceeded. Last error: {str(e)}"
                    )
                    
                logger.warning(
                    f"Request failed (attempt {self._retry_count}/{MAX_RETRIES}): {str(e)}"
                    f"\nRetrying in {RETRY_DELAY} seconds..."
                )
                await asyncio.sleep(RETRY_DELAY)
                continue
