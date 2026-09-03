import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass(frozen=True)
class APIConfig:
    """Immutable configuration container for API credentials and endpoints."""
    api_key: str
    base_url: str = "https://api.openai.com/v1/chat/completions"
    model: str = "gpt-4o-mini"
    max_retries: int = 3
    timeout: float = 30.0

    @classmethod
    def from_env(cls) -> "APIConfig":
        """Factory method to securely load configuration from environment variables."""
        load_dotenv(Path(__file__).with_name(".env"))
        key = os.environ.get("AI_PROVIDER_API_KEY")
        if not key:
            raise ValueError(
                "CRITICAL SECURITY ERROR: 'AI_PROVIDER_API_KEY' environment variable is missing."
            )
        return cls(api_key=key)