from core.models import ToolSpec, ToolParameter
from services.tool_registry import ToolRegistry
from services.agent_engine import ReActAgentEngine


# --- Define Concrete Tool Functions ---
def multiply_numbers(a: float, b: float) -> float:
    """Calculates product of two numbers."""
    return a * b


def query_system_status(service_name: str) -> str:
    """Queries live operational status of internal infrastructure services."""
    statuses = {
        "auth_db": "HEALTHY (Latency: 12ms)",
        "payment_gateway": "DEGRADED (Error Rate: 4.2%)",
        "redis_cache": "HEALTHY (Latency: 1ms)"
    }
    return statuses.get(service_name.lower(), f"UNKNOWN service '{service_name}'.")


def main() -> None:
    print("=== INITIALIZING AUTONOMOUS TOOL-USING AGENT ===\n")

    # 1. Initialize Tool Registry and Register Tools
    registry = ToolRegistry()

    registry.register_tool(ToolSpec(
        name="multiply_numbers",
        description="Multiplies two numbers together.",
        parameters=[
            ToolParameter("a", "float", "First number"),
            ToolParameter("b", "float", "Second number")
        ],
        function_ptr=multiply_numbers
    ))

    registry.register_tool(ToolSpec(
        name="query_system_status",
        description="Checks operational status of a named infrastructure service.",
        parameters=[
            ToolParameter("service_name", "string", "Target service key (e.g. auth_db, payment_gateway)")
        ],
        function_ptr=query_system_status
    ))

    # 2. Instantiate Agent Core
    agent_engine = ReActAgentEngine(registry=registry, max_iterations=4)
    system_prompt = agent_engine.build_system_prompt()

    print("--- HYDRATED AGENT SYSTEM PROMPT ---")
    print(system_prompt)

    # 3. Simulate Iterative Execution Trace (ReAct Loop)
    user_goal = "Check the status of the payment gateway service and multiply its reported error rate percentage (4.2) by 10 to calculate projected lost instances."
    print(f"--- USER GOAL: '{user_goal}' ---\n")

    # Simulated Turn 1 Model Generation
    simulated_llm_turn_1 = (
        "Thought: I need to query the status of the payment_gateway service to verify its error rate.\n"
        "Action: {\"tool_name\": \"query_system_status\", \"arguments\": {\"service_name\": \"payment_gateway\"}}"
    )

    print("[STEP 1 - LLM Generation]")
    print(simulated_llm_turn_1)

    parsed_step_1 = agent_engine.parse_llm_response(simulated_llm_turn_1)
    if parsed_step_1.action:
        observation_1 = registry.execute_action(parsed_step_1.action)
        print(f"-> [RUNTIME OBSERVATION]: {observation_1}\n")

    # Simulated Turn 2 Model Generation
    simulated_llm_turn_2 = (
        "Thought: The status report confirms an error rate of 4.2%. Now I must multiply 4.2 by 10.\n"
        "Action: {\"tool_name\": \"multiply_numbers\", \"arguments\": {\"a\": 4.2, \"b\": 10}}"
    )

    print("[STEP 2 - LLM Generation]")
    print(simulated_llm_turn_2)

    parsed_step_2 = agent_engine.parse_llm_response(simulated_llm_turn_2)
    if parsed_step_2.action:
        observation_2 = registry.execute_action(parsed_step_2.action)
        print(f"-> [RUNTIME OBSERVATION]: {observation_2}\n")

    # Simulated Turn 3 Model Generation (Final Answer)
    simulated_llm_turn_3 = (
        "Thought: I have obtained the query results and completed the calculation.\n"
        "Final Answer: The payment gateway service is currently DEGRADED with a 4.2% error rate. Multiplying this by 10 yields 42 projected lost instances."
    )

    print("[STEP 3 - LLM Generation]")
    print(simulated_llm_turn_3)

    parsed_step_3 = agent_engine.parse_llm_response(simulated_llm_turn_3)
    if parsed_step_3.is_final:
        print("\n==================================================")
        print("EXECUTION TERMINATED SUCCESSFULLY.")
        print(f"Final Agent Answer: {parsed_step_3.final_answer}")
        print("==================================================")


if __name__ == "__main__":
    main()