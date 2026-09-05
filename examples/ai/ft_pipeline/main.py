from core.models import ChatMessage, TrainingSample, LoRAConfig
from core.math_utils import estimate_vram_requirements, compute_lora_trainable_params
from services.validator import DatasetValidator
from services.lora_engine import SimulatedLoRAAdapter


def main() -> None:
    print("=== INITIALIZING FINE-TUNING PIPELINE ENGINE ===\n")

    # 1. Resource Estimation
    model_size_b = 7.0
    vram_stats = estimate_vram_requirements(model_size_b)
    print(f"--- VRAM REQUIREMENTS FOR {model_size_b}B MODEL ---")
    print(f"  Full FP16 Fine-Tuning: {vram_stats['full_sft_fp16_gb']} GB")
    print(f"  LoRA FP16 Adaptation : {vram_stats['lora_fp16_gb']} GB")
    print(f"  QLoRA 4-bit Quantized: {vram_stats['qlora_int4_gb']} GB\n")

    # 2. Dataset Processing and Validation
    samples = [
        TrainingSample(
            sample_id="SFT-001",
            messages=[
                ChatMessage(role="system", content="You are a SQL generation agent."),
                ChatMessage(role="user", content="Fetch active users created in 2026."),
                ChatMessage(role="assistant", content="SELECT * FROM users WHERE status = 'active' AND YEAR(created_at) = 2026;")
            ]
        ),
        TrainingSample(
            sample_id="SFT-002",
            messages=[
                ChatMessage(role="system", content="You are a SQL generation agent."),
                ChatMessage(role="user", content=""),  # Invalid empty content
                ChatMessage(role="assistant", content="SELECT 1;")
            ]
        )
    ]

    validator = DatasetValidator(max_seq_length=1024)
    print("--- DATASET VALIDATION AUDIT ---")
    for sample in samples:
        is_valid, msg = validator.validate_sample(sample)
        status = "PASS" if is_valid else "FAIL"
        print(f"  Sample ID '{sample.sample_id}': [{status}] {msg}")

    # 3. LoRA Parameter Injection Analysis
    print("\n--- LORA ADAPTER PARAMETER CALCULATION ---")
    lora_config = LoRAConfig(target_rank_r=16, alpha=32, target_modules=["q_proj", "v_proj"])
    
    # Llama-3-8B hidden dimension: 4096, 32 Transformer layers
    hidden_dim = 4096
    num_layers = 32
    target_modules_count = len(lora_config.target_modules)

    trainable_params = compute_lora_trainable_params(
        hidden_dim=hidden_dim,
        rank_r=lora_config.target_rank_r,
        target_module_count=target_modules_count,
        num_layers=num_layers
    )

    base_params = 8_000_000_000
    percentage = (trainable_params / base_params) * 100

    print(f"  Base Model Parameters: {base_params:,}")
    print(f"  Trainable LoRA Params: {trainable_params:,}")
    print(f"  Trainable Ratio      : {percentage:.4f}% of total weights")

    # 4. Simulate Adapter Matrix Initialization
    adapter = SimulatedLoRAAdapter(in_dim=hidden_dim, out_dim=hidden_dim, config=lora_config)
    print(f"  Scaling Factor (alpha/r): {adapter.compute_scaling_factor()}")


if __name__ == "__main__":
    main()