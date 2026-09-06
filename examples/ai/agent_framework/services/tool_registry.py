from core.models import ToolSpec, ActionCall


class ToolRegistry:
    """Manages tool registrations, JSON Schema generation, and function dispatching."""

    def __init__(self) -> None:
        self._tools: dict[str, ToolSpec] = {}

    def register_tool(self, spec: ToolSpec) -> None:
        """Registers a executable tool spec into the central registry."""
        self._tools[spec.name] = spec

    def get_registered_tools_prompt(self) -> str:
        """Generates structured documentation block describing available tools for prompts."""
        tool_descriptions = []
        for name, spec in self._tools.items():
            params_desc = ", ".join([f"{p.name}: {p.param_type}" for p in spec.parameters])
            tool_descriptions.append(f"- {name}({params_desc}): {spec.description}")
        return "\n".join(tool_descriptions)

    def execute_action(self, action: ActionCall) -> str:
        """Dispatches action calls to their target registered function implementations."""
        if action.tool_name not in self._tools:
            return f"ERROR: Tool '{action.tool_name}' is not registered in environment."

        spec = self._tools[action.tool_name]
        try:
            # Execute underlying Python function pointer with provided arguments
            result = spec.function_ptr(**action.arguments)
            return str(result)
        except Exception as exc:
            return f"ERROR executing tool '{action.tool_name}': {str(exc)}"