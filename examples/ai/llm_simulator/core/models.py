from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class TokenSequence:
    """Represents a tokenized text sequence with text-to-integer mappings."""
    
    raw_text: str
    token_ids: List[int]


@dataclass
class SamplingConfig:
    """Controls generation behavior during token prediction."""
    
    temperature: float = 1.0  # Higher values increase output variance
    top_k: int = 3            # Restricts sampling to top K candidate tokens
    max_context_window: int = 8  # Enforces maximum context token limit


@dataclass
class PredictionOutput:
    """Contains sampled token output and context state."""
    
    generated_token_id: int
    generated_text: str
    probabilities: Dict[str, float]
    active_context_ids: List[int]