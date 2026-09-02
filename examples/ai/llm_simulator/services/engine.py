import math
import random
from core.models import SamplingConfig, PredictionOutput
from services.tokenizer import DictionaryTokenizer


class LanguageModelEngine:
    """Simulates a Causal Autoregressive LLM with Context Truncation and Sampling."""

    def __init__(self, tokenizer: DictionaryTokenizer) -> None:
        self.tokenizer = tokenizer
        
        # Transition probability matrix: P(Next_Token | Last_Token_ID)
        # Simulates pretrained attention weights
        self._n_gram_weights: dict[int, dict[int, float]] = {
            2: {3: 4.0, 8: 1.0},        # "system" -> "status" (high), "error" (low)
            3: {4: 5.0},                 # "status" -> "is"
            4: {5: 4.0, 6: 2.0, 7: 1.0}, # "is" -> "nominal" (high), "degraded", "critical"
            8: {9: 3.5},                 # "error" -> "detected"
        }

    def _truncate_context(self, token_ids: list[int], max_window: int) -> list[int]:
        """Enforces context window boundaries by keeping only the most recent N tokens."""
        if len(token_ids) > max_window:
            return token_ids[-max_window:]
        return token_ids

    def _compute_softmax(self, logits: dict[int, float], temperature: float) -> dict[int, float]:
        """Applies Temperature scaling and computes Softmax probabilities over logits."""
        # Avoid division by zero
        temp = max(temperature, 1e-5)
        
        # Temperature scaling: z_i / T
        scaled_logits = {tid: val / temp for tid, val in logits.items()}
        
        # Numerical stability shift
        max_logit = max(scaled_logits.values())
        exp_logits = {tid: math.exp(val - max_logit) for tid, val in scaled_logits.items()}
        sum_exp = sum(exp_logits.values())
        
        return {tid: val / sum_exp for tid, val in exp_logits.items()}

    def generate_next_token(self, context_ids: list[int], config: SamplingConfig) -> PredictionOutput:
        """Executes one autoregressive pass over truncated context."""
        # 1. Enforce Context Window Truncation
        active_context = self._truncate_context(context_ids, config.max_context_window)
        
        if not active_context:
            raise ValueError("Context vector cannot be empty.")

        # 2. Extract last token to simulate auto-regressive next-step processing
        last_token_id = active_context[-1]
        raw_logits = self._n_gram_weights.get(last_token_id, {1: 1.0})  # Fallback to <UNK>

        # 3. Softmax with Temperature
        probabilities = self._compute_softmax(raw_logits, config.temperature)

        # 4. Apply Top-K Filtering
        sorted_candidates = sorted(probabilities.items(), key=lambda x: x[1], reverse=True)[:config.top_k]
        
        # Renormalize Top-K probabilities
        top_k_sum = sum(prob for _, prob in sorted_candidates)
        renormalized = [(tid, prob / top_k_sum) for tid, prob in sorted_candidates]

        # 5. Probabilistic Sampling
        r = random.random()
        cumulative = 0.0
        selected_id = renormalized[-1][0]
        
        for tid, prob in renormalized:
            cumulative += prob
            if r <= cumulative:
                selected_id = tid
                break

        # Construct labeled probability dict for inspection
        prob_distribution = {
            self.tokenizer.decode([tid]): round(prob, 4) 
            for tid, prob in probabilities.items()
        }

        return PredictionOutput(
            generated_token_id=selected_id,
            generated_text=self.tokenizer.decode([selected_id]),
            probabilities=prob_distribution,
            active_context_ids=active_context
        )