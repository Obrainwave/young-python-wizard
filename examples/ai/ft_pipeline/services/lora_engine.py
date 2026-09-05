import random
from core.models import LoRAConfig


class SimulatedLoRAAdapter:
    """Simulates low-rank matrix initialization and weight merging logic."""

    def __init__(self, in_dim: int, out_dim: int, config: LoRAConfig) -> None:
        self.in_dim = in_dim
        self.out_dim = out_dim
        self.config = config

        # Initialize Matrix A with Gaussian random noise, Matrix B with Zeros
        self.matrix_A = [
            [random.gauss(0, 0.02) for _ in range(self.in_dim)]
            for _ in range(config.target_rank_r)
        ]
        self.matrix_B = [
            [0.0 for _ in range(config.target_rank_r)]
            for _ in range(self.out_dim)
        ]

    def get_adapter_param_count(self) -> int:
        """Calculates total trainable parameter size for this adapter pair."""
        params_A = self.config.target_rank_r * self.in_dim
        params_B = self.out_dim * self.config.target_rank_r
        return params_A + params_B

    def compute_scaling_factor(self) -> float:
        """Returns scaling hyperparameter ratio alpha / r."""
        return self.config.alpha / self.config.target_rank_r