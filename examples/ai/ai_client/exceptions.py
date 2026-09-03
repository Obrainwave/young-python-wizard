class AIClientError(Exception):
    """Base exception for all AI API client failures."""
    pass

class RateLimitExceededError(AIClientError):
    """Raised when 429 status code is returned and retries are exhausted."""
    pass

class AuthenticationError(AIClientError):
    """Raised when API key authentication fails (401/403)."""
    pass

class APIResponseError(AIClientError):
    """Raised when non-200 HTTP response status is returned."""
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        super().__init__(f"API Error [{status_code}]: {message}")