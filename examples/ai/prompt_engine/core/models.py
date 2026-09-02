from dataclasses import dataclass, field


@dataclass
class Exemplar:
    """Represents a single few-shot input/output demonstration pair."""
    input_text: str
    target_output: str


@dataclass
class PromptContext:
    """Encapsulates dynamic runtime parameters and grounding data."""
    system_role: str
    user_query: str
    grounding_docs: list[str] = field(default_factory=list)
    exemplars: list[Exemplar] = field(default_factory=list)
    output_schema_json: str | None = None