import json
import re
from typing import Any


class ResponseValidator:
    """Sanitizes and validates model outputs against JSON constraints."""

    @staticmethod
    def extract_and_parse_json(raw_response: str) -> tuple[bool, dict[str, Any], str]:
        """Extracts JSON payload from potential raw markdown strings and validates syntax."""
        # Clean markdown code block wraps if present
        cleaned = re.sub(r"```json\s*", "", raw_response)
        cleaned = re.sub(r"```\s*$", "", cleaned).strip()

        try:
            parsed = json.loads(cleaned)
            return True, parsed, "Success"
        except json.JSONDecodeError as e:
            return False, {}, f"JSON Parsing Error: {str(e)}"