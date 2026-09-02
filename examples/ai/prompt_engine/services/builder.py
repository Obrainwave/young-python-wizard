from core.models import PromptContext, Exemplar


class PromptBuilder:
    """Assembles structured, XML-delimited production prompts."""

    @staticmethod
    def build_system_prompt(context: PromptContext) -> str:
        """Constructs the system prompt including persona framing and schema constraints."""
        components = [
            f"<system_role>\n{context.system_role}\n</system_role>"
        ]

        if context.output_schema_json:
            schema_directive = (
                "<output_instructions>\n"
                "Your output MUST strictly conform to the following JSON Schema.\n"
                "Do not include Markdown formatting blocks or preamble text.\n"
                f"JSON Schema:\n{context.output_schema_json}\n"
                "</output_instructions>"
            )
            components.append(schema_directive)

        return "\n\n".join(components)

    @staticmethod
    def build_user_prompt(context: PromptContext) -> str:
        """Assembles context documents, few-shot exemplars, and the user query."""
        sections = []

        # 1. Inject Grounding Documents
        if context.grounding_docs:
            docs_block = ["<grounding_context>"]
            for idx, doc in enumerate(context.grounding_docs, start=1):
                docs_block.append(f'  <document id="{idx}">\n    {doc}\n  </document>')
            docs_block.append("</grounding_context>")
            sections.append("\n".join(docs_block))

        # 2. Inject Few-Shot Exemplars
        if context.exemplars:
            exemplar_block = ["<few_shot_examples>"]
            for idx, ex in enumerate(context.exemplars, start=1):
                exemplar_block.append(
                    f'  <example id="{idx}">\n'
                    f'    <input>{ex.input_text}</input>\n'
                    f'    <output>{ex.target_output}</output>\n'
                    f'  </example>'
                )
            exemplar_block.append("</few_shot_examples>")
            sections.append("\n".join(exemplar_block))

        # 3. Inject Target User Input
        sections.append(
            f"<user_request>\n{context.user_query}\n</user_request>"
        )

        return "\n\n".join(sections)