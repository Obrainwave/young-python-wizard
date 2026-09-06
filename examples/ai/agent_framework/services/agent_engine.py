import json
import re
from core.models import ActionCall, AgentStepResult
from services.tool_registry import ToolRegistry


class ReActAgentEngine:
    """Orchestrates the ReAct reasoning, acting, and observation loop."""

    def __init__(self, registry: ToolRegistry, max_iterations: int = 5) -> None:
        self.registry = registry
        self.max_iterations = max_iterations

    def build_system_prompt(self) -> str:
        """Constructs system prompt containing tool schemas and ReAct format constraints."""
        tools_block = self.registry.get_registered_tools_prompt()
        return (
            "You are an autonomous problem-solving agent. Solve user requests using the ReAct loop.\n"
            "Available Tools:\n"
            f"{tools_block}\n\n"
            "Use the following structure for your responses:\n"
            "Thought: <Your reasoning steps about what to do next>\n"
            "Action: <JSON string containing tool_name and arguments OR 'None'>\n"
            "Final Answer: <Your ultimate response when target objective is completed>\n"
            "Note: Format 'Action' as strict JSON: {\"tool_name\": \"...\", \"arguments\": {...}}\n"
        )

    def parse_llm_response(self, response_text: str) -> AgentStepResult:
        """Parses model string outputs into structured Thought, Action, and Final Answer states."""
        thought_match = re.search(r"Thought:\s*(.*?)(?=\nAction:|\nFinal Answer:|$)", response_text, re.DOTALL)
        thought = thought_match.group(1).strip() if thought_match else "Analyzing current state."

        # Check for Final Answer termination condition
        final_match = re.search(r"Final Answer:\s*(.*)", response_text, re.DOTALL)
        if final_match:
            return AgentStepResult(
                thought=thought,
                is_final=True,
                final_answer=final_match.group(1).strip()
            )

        # Parse Action JSON payload
        action_match = re.search(r"Action:\s*(\{.*?\})", response_text, re.DOTALL)
        if action_match:
            try:
                action_data = json.loads(action_match.group(1))
                action_call = ActionCall(
                    tool_name=action_data.get("tool_name", ""),
                    arguments=action_data.get("arguments", {})
                )
                return AgentStepResult(thought=thought, action=action_call)
            except json.JSONDecodeError:
                pass

        return AgentStepResult(thought=thought, observation="Parse Error: Invalid Action JSON format.")