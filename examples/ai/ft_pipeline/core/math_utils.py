def estimate_vram_requirements(param_count_billions: float) -> dict[str, float]:
    """Calculates estimated VRAM footprint (in GB) across fine-tuning modes."""
    full_sft = param_count_billions * 16.0  # FP16 + AdamW optimizer states
    lora_fp16 = param_count_billions * 4.0  # Base FP16 + small trainable state
    qlora_int4 = (param_count_billions * 0.75) + 4.0  # 4-bit base + activation buffer

    return {
        "full_sft_fp16_gb": round(full_sft, 2),
        "lora_fp16_gb": round(lora_fp16, 2),
        "qlora_int4_gb": round(qlora_int4, 2)
    }


def compute_lora_trainable_params(
    hidden_dim: int, rank_r: int, target_module_count: int, num_layers: int
) -> int:
    """
    Computes exact parameter count added by LoRA matrices B and A.
    For each target matrix W (d x d), LoRA injects B (d x r) and A (r x d).
    """
    params_per_matrix = (hidden_dim * rank_r) + (rank_r * hidden_dim)
    return params_per_matrix * target_module_count * num_layers