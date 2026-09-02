from core.models import PromptContext, Exemplar
from services.builder import PromptBuilder
from services.validator import ResponseValidator


def main() -> None:
    print("=== PRODUCTION PROMPT ENGINE HYDRATION ===\n")

    # Define Output Schema Contract
    json_schema = """{
  "type": "object",
  "properties": {
    "incident_id": {"type": "string"},
    "severity": {"type": "string", "enum": ["LOW", "MEDIUM", "HIGH", "CRITICAL"]},
    "root_cause_summary": {"type": "string"}
  },
  "required": ["incident_id", "severity", "root_cause_summary"]
}"""

    # Define Few-Shot Exemplar
    sample_exemplar = Exemplar(
        input_text="[ERR-9021] Redis connection timeout on cluster node 4. High memory fragmentation detected.",
        target_output='{"incident_id": "INC-9021", "severity": "HIGH", "root_cause_summary": "Redis cluster node 4 memory fragmentation causing socket timeouts."}'
    )

    # Initialize Context
    context = PromptContext(
        system_role="You are an Site Reliability Engineering Incident Responder. Analyze raw log strings and format structured incident reports.",
        user_query="[ERR-1044] PostgreSQL Primary DB connection pool exhausted. 150 incoming queries blocked on port 5432.",
        grounding_docs=[
            "Standard Operating Procedure: Connection pool depletion indicates thread starvation or leaked DB client instances."
        ],
        exemplars=[sample_exemplar],
        output_schema_json=json_schema
    )

    # Assemble Prompts
    system_prompt = PromptBuilder.build_system_prompt(context)
    user_prompt = PromptBuilder.build_user_prompt(context)

    print("--- HYDRATED SYSTEM PROMPT ---")
    print(system_prompt)
    print("\n--- HYDRATED USER PROMPT ---")
    print(user_prompt)

    # Simulate Model Inference Output
    simulated_llm_output = """```json
{
  "incident_id": "INC-1044",
  "severity": "CRITICAL",
  "root_cause_summary": "Database connection pool exhaustion on primary PostgreSQL node leading to request blocking."
}
```"""

    print("\n--- SIMULATED MODEL OUTPUT ---")
    print(simulated_llm_output)

    # Validate Output
    is_valid, data, msg = ResponseValidator.extract_and_parse_json(simulated_llm_output)
    print("\n--- VALIDATION RESULT ---")
    print(f"Status:  {'PASS' if is_valid else 'FAIL'}")
    print(f"Parsed Object: {data}")


if __name__ == "__main__":
    main()