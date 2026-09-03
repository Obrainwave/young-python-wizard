from config import APIConfig
from client import ResilientAIClient
from exceptions import AIClientError


def main() -> None:

    print("=== INITIALIZING AI API CLIENT PIPELINE ===\n")

    try:
        config = APIConfig.from_env()
        client = ResilientAIClient(config)

        messages = [
            {"role": "system", "content": "You are a concise DevOps engineer."},
            {"role": "user", "content": "What is the function of a reverse proxy in web architectures?"}
        ]

        print(f"Submitting request to model: '{config.model}'...")
        # Note: In a live environment with a valid key, this executes an actual inference call
        response = client.generate_completion(messages)
        print("Response Content:\n", response["choices"][0]["message"]["content"])
        # print("[SUCCESS] Client initialized and payload validated successfully.")

    except AIClientError as err:
        print(f"[ERROR] Execution failed: {str(err)}")
    except Exception as exc:
        print(f"[UNEXPECTED ERROR]: {str(exc)}")


if __name__ == "__main__":
    main()