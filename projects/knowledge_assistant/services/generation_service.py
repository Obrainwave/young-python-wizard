import os

class GenerationService:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")

    def generate(self, question, context_chunks):
        context = "\n\n".join([chunk.content for chunk in context_chunks])
        if self.api_key:
            return self._generate_with_openai(question, context)
        else:
            return self._generate_mock(question, context_chunks)

    def _generate_with_openai(self, question, context):
        import openai
        openai.api_key = self.api_key
        prompt = f"""You are a helpful knowledge assistant. Answer the user's question based ONLY on the provided context.
If the answer is not in the context, say "I cannot answer based on the provided documents."

Context:
{context}

Question: {question}

Answer:"""
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful knowledge assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=200
        )
        return response.choices[0].message.content.strip()

    def _generate_mock(self, question, context_chunks):
        """Simple fallback: return the first relevant chunk."""
        if not context_chunks:
            return "I cannot answer based on the provided documents."
        return f"Based on the documents:\n{context_chunks[0].content[:500]}"