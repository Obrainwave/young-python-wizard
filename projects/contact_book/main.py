from storage.database import Database
from storage.initializer import DatabaseInitializer
from services.contact_service import ContactService

def main():
    db = Database("contacts.db")
    db.connect()
    DatabaseInitializer(db).initialize()
    service = ContactService(db)

    while True:
        print("\n--- Contact Book ---")
        print("1. Add Contact")
        print("2. View All Contacts")
        print("3. Search Contacts")
        print("4. Update Contact")
        print("5. Delete Contact")
        print("6. Exit")
        choice = input("Choose: ").strip()

        try:
            if choice == "1":
                name = input("Name: ")
                phone = input("Phone: ")
                email = input("Email: ")
                address = input("Address: ")
                contact = service.add_contact(name, phone, email, address)
                print(f"Contact added with ID {contact.id}")
            elif choice == "2":
                contacts = service.get_all_contacts()
                if not contacts:
                    print("No contacts found.")
                else:
                    print("\nContacts:")
                    for c in contacts:
                        print(f"ID: {c.id}")
                        print(f"  Name: {c.name}")
                        print(f"  Phone: {c.phone or 'N/A'}")
                        print(f"  Email: {c.email or 'N/A'}")
                        print(f"  Address: {c.address or 'N/A'}")
                        print()
            elif choice == "3":
                term = input("Search term: ")
                results = service.search_contacts(term)
                if not results:
                    print("No matches.")
                else:
                    print("\nSearch Results:")
                    for c in results:
                        print(f"ID: {c.id} - {c.name} - {c.phone} - {c.email}")
            elif choice == "4":
                contact_id = int(input("Contact ID to update: "))
                name = input("New name (leave blank to keep current): ")
                phone = input("New phone (leave blank to keep current): ")
                email = input("New email (leave blank to keep current): ")
                address = input("New address (leave blank to keep current): ")
                # Get current contact to fill blanks
                current = service.get_contact(contact_id)
                if not current:
                    print("Contact not found.")
                    continue
                new_name = name if name.strip() else current.name
                new_phone = phone if phone.strip() else current.phone
                new_email = email if email.strip() else current.email
                new_address = address if address.strip() else current.address
                service.update_contact(contact_id, new_name, new_phone, new_email, new_address)
                print("Contact updated.")
            elif choice == "5":
                contact_id = int(input("Contact ID to delete: "))
                service.delete_contact(contact_id)
                print("Contact deleted.")
            elif choice == "6":
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