from core.models import TrainingSample


class DatasetValidator:
    """Validates structural integrity and token limits of training datasets."""

    def __init__(self, max_seq_length: int = 2048) -> None:
        self.max_seq_length = max_seq_length

    def validate_sample(self, sample: TrainingSample) -> tuple[bool, str]:
        """Validates role sequencing and approximate sequence length."""
        if not sample.messages:
            return False, "Sample contains empty message sequence."

        valid_roles = {"system", "user", "assistant"}
        total_char_length = 0

        for msg in sample.messages:
            if msg.role not in valid_roles:
                return False, f"Invalid role detected: '{msg.role}'."
            if not msg.content.strip():
                return False, f"Empty content payload for role '{msg.role}'."
            total_char_length += len(msg.content)

        # Approximate token count (1 token ~= 4 chars)
        approx_tokens = total_char_length / 4.0
        if approx_tokens > self.max_seq_length:
            return False, f"Sequence length (~{approx_tokens:.0f} tokens) exceeds limit ({self.max_seq_length})."

        return True, "Valid"