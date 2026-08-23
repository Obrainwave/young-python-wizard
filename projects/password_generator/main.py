from storage.database import Database
from storage.initializer import DatabaseInitializer
from services.password_service import PasswordService

def get_yes_no(prompt):
    """Helper to get a yes/no answer from the user."""
    while True:
        ans = input(prompt).strip().lower()
        if ans in ('y', 'yes'):
            return True
        elif ans in ('n', 'no'):
            return False
        else:
            print("Please enter 'yes' or 'no'.")

def main():
    db = Database("password_history.db")
    db.connect()
    DatabaseInitializer(db).initialize()
    service = PasswordService(db)

    while True:
        print("\n--- Password Generator ---")
        print("1. Generate new password")
        print("2. View history")
        print("3. Clear history")
        print("4. Exit")
        choice = input("Choose: ").strip()

        try:
            if choice == "1":
                length = int(input("Password length: "))
                use_upper = get_yes_no("Include uppercase letters? (yes/no): ")
                use_digits = get_yes_no("Include digits? (yes/no): ")
                use_special = get_yes_no("Include special characters? (yes/no): ")
                password = service.generate_password(length, use_upper, use_digits, use_special)
                print(f"\nGenerated password: {password}")
            elif choice == "2":
                history = service.get_history()
                if not history:
                    print("No history yet.")
                else:
                    print("\nPassword History (newest first):")
                    for entry in history:
                        print(f"[{entry.created_at}] Length: {entry.length}, "
                              f"Types: {entry.char_types}, Password: {entry.password}")
            elif choice == "3":
                service.clear_history()
                print("History cleared.")
            elif choice == "4":
                print("Goodbye!")
                break
            else:
                print("Invalid option.")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    db.close()

if __name__ == "__main__":
    main()