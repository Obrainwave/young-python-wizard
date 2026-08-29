from storage.file_storage import FileStorage
from services.journal_service import JournalService

def main():
    storage = FileStorage("journal.json")
    storage.ensure_file_exists()
    service = JournalService(storage)

    while True:
        print("\n--- Journal App ---")
        print("1. New Entry")
        print("2. View All Entries")
        print("3. View Single Entry")
        print("4. Search Entries")
        print("5. Edit Entry")
        print("6. Delete Entry")
        print("7. Exit")
        choice = input("Choose: ").strip()

        try:
            if choice == "1":
                title = input("Title: ")
                content = input("Content: ")
                tags_input = input("Tags (comma separated, optional): ")
                tags = [t.strip() for t in tags_input.split(",") if t.strip()]
                entry = service.create_entry(title, content, tags)
                print(f"Entry created with ID {entry.id}")
            elif choice == "2":
                entries = service.get_all_entries()
                if not entries:
                    print("No entries yet.")
                else:
                    print("\nAll Entries:")
                    for e in entries:
                        print(f"ID: {e.id} | {e.title} | {e.timestamp}")
            elif choice == "3":
                entry_id = int(input("Enter entry ID: "))
                entry = service.get_entry_by_id(entry_id)
                if entry:
                    print(f"\nID: {entry.id}")
                    print(f"Title: {entry.title}")
                    print(f"Timestamp: {entry.timestamp}")
                    print(f"Tags: {', '.join(entry.tags) if entry.tags else 'None'}")
                    print(f"Content:\n{entry.content}")
                else:
                    print("Entry not found.")
            elif choice == "4":
                term = input("Search term: ")
                results = service.search_entries(term)
                if not results:
                    print("No matching entries.")
                else:
                    print("\nSearch Results:")
                    for e in results:
                        print(f"ID: {e.id} | {e.title} | {e.timestamp}")
            elif choice == "5":
                entry_id = int(input("Enter entry ID to edit: "))
                entry = service.get_entry_by_id(entry_id)
                if not entry:
                    print("Entry not found.")
                    continue
                print("Leave blank to keep current value.")
                new_title = input(f"New title [{entry.title}]: ").strip()
                new_content = input(f"New content [{entry.content}]: ").strip()
                tags_input = input(f"New tags (comma separated) [{', '.join(entry.tags)}]: ").strip()
                tags = [t.strip() for t in tags_input.split(",") if t.strip()] if tags_input else None
                updated = service.update_entry(
                    entry_id,
                    title=new_title if new_title else None,
                    content=new_content if new_content else None,
                    tags=tags
                )
                print(f"Entry {updated.id} updated.")
            elif choice == "6":
                entry_id = int(input("Enter entry ID to delete: "))
                if service.delete_entry(entry_id):
                    print("Entry deleted.")
                else:
                    print("Entry not found.")
            elif choice == "7":
                print("Goodbye!")
                break
            else:
                print("Invalid option.")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()