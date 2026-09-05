from dataclasses import dataclass, field


@dataclass
class ChatMessage:
    """Represents a single conversation turn in ChatML format."""
    role: str  # 'system', 'user', or 'assistant'
    content: str


@dataclass
class TrainingSample:
    """Represents a complete training instance."""
    sample_id: str
    messages: list[ChatMessage]


@dataclass
class LoRAConfig:
    """Configuration parameter container for Low-Rank Adaptation."""
    target_rank_r: int = 16
    alpha: int = 32
    target_modules: list[str] = field(default_factory=lambda: ["q_proj", "v_proj"])
    dropout: float = 0.05