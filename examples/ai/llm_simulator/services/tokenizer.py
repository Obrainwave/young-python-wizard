from typing import Dict, List
from core.models import TokenSequence


class DictionaryTokenizer:
    """A sub-word dictionary tokenizer simulating BPE vocabulary lookups."""

    def __init__(self) -> None:
        # Vocabulary mapping tokens to discrete numerical IDs
        self.vocab: Dict[str, int] = {
            "<PAD>": 0,
            "<UNK>": 1,
            "system": 2,
            "status": 3,
            "is": 4,
            "nominal": 5,
            "degraded": 6,
            "critical": 7,
            "error": 8,
            "detected": 9,
        }
        self.inverse_vocab: Dict[int, str] = {v: k for k, v in self.vocab.items()}

    def encode(self, text: str) -> TokenSequence:
        """Converts raw input string into token IDs."""
        words = text.lower().strip().split()
        token_ids = []
        for word in words:
            token_id = self.vocab.get(word, self.vocab["<UNK>"])
            token_ids.append(token_id)

        return TokenSequence(raw_text=text, token_ids=token_ids)

    def decode(self, token_ids: List[int]) -> str:
        """Decodes integer token IDs back into string space."""
        words = [self.inverse_vocab.get(tid, "<UNK>") for tid in token_ids]
        return " ".join(words)