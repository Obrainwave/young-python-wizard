import secrets
import string
from datetime import datetime
from storage.password_history_repository import PasswordHistoryRepository
from models.password_history import PasswordHistory

class PasswordService:
    def __init__(self, db):
        self.repo = PasswordHistoryRepository(db)

    def generate_password(self, length, use_uppercase, use_digits, use_special):
        """
        Generate a random password with the specified character sets.

        Args:
            length (int): Desired password length.
            use_uppercase (bool): Include uppercase letters.
            use_digits (bool): Include digits.
            use_special (bool): Include special characters.

        Returns:
            str: The generated password.

        Raises:
            ValueError: If no character set is selected or length < 1.
        """
        if length < 1:
            raise ValueError("Password length must be at least 1.")

        # Build the character pool
        char_pool = string.ascii_lowercase  # always include lowercase
        char_types = ["lowercase"]

        if use_uppercase:
            char_pool += string.ascii_uppercase
            char_types.append("uppercase")
        if use_digits:
            char_pool += string.digits
            char_types.append("digits")
        if use_special:
            char_pool += string.punctuation
            char_types.append("special")

        if len(char_pool) == 0:
            raise ValueError("At least one character set must be selected.")

        # Use secrets.choice for cryptographically secure randomness
        password = ''.join(secrets.choice(char_pool) for _ in range(length))

        # Store in history
        self._save_to_history(password, length, char_types)

        return password

    def _save_to_history(self, password, length, char_types):
        """Save the generated password to the history."""
        char_types_str = ",".join(char_types)
        created_at = datetime.now().isoformat(timespec='seconds')
        entry = PasswordHistory(
            password=password,
            length=length,
            char_types=char_types_str,
            created_at=created_at
        )
        self.repo.insert(entry)

    def get_history(self):
        """Return the full password history."""
        return self.repo.get_all()

    def clear_history(self):
        """Delete all password history."""
        self.repo.delete_all()