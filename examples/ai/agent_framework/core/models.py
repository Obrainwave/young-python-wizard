from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class ToolParameter:
    """Describes a single tool function parameter."""
    name: str
    param_type: str
    description: str
    required: bool = True


@dataclass
class ToolSpec:
    """Specification metadata for exposing python functions to the LLM."""
    name: str
    description: str
    parameters: list[ToolParameter]
    function_ptr: Callable


@dataclass
class ActionCall:
    """Represents a tool invocation intent emitted by the agent core."""
    tool_name: str
    arguments: dict[str, Any]


@dataclass
class AgentStepResult:
    """Container for intermediate ReAct reasoning steps."""
    thought: str
    action: ActionCall | None = None
    observation: str | None = None
    is_final: bool = False
    final_answer: str | None = None