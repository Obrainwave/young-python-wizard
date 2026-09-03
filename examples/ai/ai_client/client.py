import time
import random
import httpx
from typing import Any
from config import APIConfig
from exceptions import RateLimitExceededError, AuthenticationError, APIResponseError, AIClientError


class ResilientAIClient:
    """Production-grade HTTP client featuring automated retries and exponential backoff."""

    def __init__(self, config: APIConfig) -> None:
        self.config = config
        self.headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json"
        }

    def generate_completion(self, messages: list[dict[str, str]], temperature: float = 0.3) -> dict[str, Any]:
        """Submits inference payload with exponential backoff and error handling."""
        payload = {
            "model": self.config.model,
            "messages": messages,
            "temperature": temperature
        }

        base_delay = 1.0  # Initial delay in seconds
        max_delay = 10.0

        for attempt in range(1, self.config.max_retries + 1):
            try:
                with httpx.Client(timeout=self.config.timeout) as client:
                    response = client.post(self.config.base_url, headers=self.headers, json=payload)
                    
                    # Handle successful response
                    if response.status_code == 200:
                        return response.json()

                    # Handle specific failure status codes
                    if response.status_code in (401, 403):
                        raise AuthenticationError("Invalid or unauthorized API key provided.")
                    
                    if response.status_code == 429:
                        if attempt == self.config.max_retries:
                            raise RateLimitExceededError("Rate limit exceeded. Maximum retries reached.")
                        # Calculate backoff with jitter
                        jitter = random.uniform(0, 0.5)
                        sleep_time = min(max_delay, (base_delay * (2 ** (attempt - 1))) + jitter)
                        print(f"[WARN] Rate limited (429). Retrying in {sleep_time:.2f}s (Attempt {attempt}/{self.config.max_retries})...")
                        time.sleep(sleep_time)
                        continue

                    # Fallthrough for other error status codes
                    raise APIResponseError(response.status_code, response.text)

            except httpx.RequestError as exc:
                if attempt == self.config.max_retries:
                    raise AIClientError(f"Network transport error: {str(exc)}")
                sleep_time = base_delay * attempt
                print(f"[WARN] Network error encountered. Retrying in {sleep_time:.2f}s...")
                time.sleep(sleep_time)

        raise AIClientError("Unexpected client termination without response.")