from core.models import SamplingConfig
from services.tokenizer import DictionaryTokenizer
from services.engine import LanguageModelEngine


def main() -> None:
    print("=== AUTOREGRESSIVE LLM INFERENCE SIMULATOR ===\n")

    tokenizer = DictionaryTokenizer()
    engine = LanguageModelEngine(tokenizer)

    prompt = "System status is"
    encoded_input = tokenizer.encode(prompt)
    
    print(f"Input Prompt:  '{prompt}'")
    print(f"Token IDs:     {encoded_input.token_ids}\n")

    # Configure sampling parameters
    config = SamplingConfig(temperature=0.7, top_k=2, max_context_window=4)

    # Generate 2 subsequent tokens
    current_context = list(encoded_input.token_ids)
    
    for step in range(2):
        output = engine.generate_next_token(current_context, config)
        
        print(f"--- Generation Step {step + 1} ---")
        print(f"Active Context (Truncated): {output.active_context_ids}")
        print(f"Predicted Logit Softmax:   {output.probabilities}")
        print(f"Sampled Next Token:        '{output.generated_text}' (ID: {output.generated_token_id})\n")
        
        # Append selected token back into context loop (Autoregressive step)
        current_context.append(output.generated_token_id)

    final_text = tokenizer.decode(current_context)
    print(f"Final Generated Sequence: '{final_text}'")


if __name__ == "__main__":
    main()