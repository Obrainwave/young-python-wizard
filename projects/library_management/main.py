from storage.database import Database
from storage.initializer import DatabaseInitializer
from services.library_service import LibraryService

def main():
    db = Database("library.db")
    db.connect()
    DatabaseInitializer(db).initialize()
    service = LibraryService(db)

    while True:
        print("\n--- Library Management System ---")
        print("1. Manage Books")
        print("2. Manage Members")
        print("3. Borrow Book")
        print("4. Return Book")
        print("5. View Overdue Loans")
        print("6. Exit")
        choice = input("Choose: ").strip()

        try:
            if choice == "1":
                manage_books(service)
            elif choice == "2":
                manage_members(service)
            elif choice == "3":
                borrow_book_ui(service)
            elif choice == "4":
                return_book_ui(service)
            elif choice == "5":
                overdue = service.get_overdue_loans()
                if not overdue:
                    print("No overdue loans.")
                else:
                    for loan in overdue:
                        print(f"Loan ID: {loan.id} - Book ID: {loan.book_id} - Due: {loan.due_date}")
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

def manage_books(service):
    while True:
        print("\n--- Manage Books ---")
        print("1. Add Book")
        print("2. Search Books")
        print("3. List All Books")
        print("4. Update Book Info")
        print("5. Add/Update Cover")
        print("6. Delete Book")
        print("7. Back")
        choice = input("Choose: ").strip()
        if choice == "1":
            title = input("Title: ")
            author = input("Author: ")
            isbn = input("ISBN (optional): ")
            cover = input("Cover image path (optional, leave blank for none): ")
            if cover.strip():
                book = service.add_book(title, author, isbn, cover.strip())
            else:
                book = service.add_book(title, author, isbn)
            print(f"Book added with ID {book.id}")
        elif choice == "2":
            term = input("Search term: ")
            books = service.search_books(term)
            for b in books:
                status = "Available" if b.available else "Borrowed"
                cover = "Has cover" if b.cover_path else "No cover"
                print(f"ID: {b.id} | {b.title} by {b.author} | {status} | {cover}")
        elif choice == "3":
            books = service.get_all_books()
            for b in books:
                status = "Available" if b.available else "Borrowed"
                cover = "Has cover" if b.cover_path else "No cover"
                print(f"ID: {b.id} | {b.title} by {b.author} | {status} | {cover}")
        elif choice == "4":
            book_id = int(input("Book ID to update: "))
            title = input("New title: ")
            author = input("New author: ")
            isbn = input("New ISBN: ")
            service.update_book(book_id, title, author, isbn)
            print("Book updated.")
        elif choice == "5":
            book_id = int(input("Book ID: "))
            cover = input("Cover image path: ")
            service.update_book_cover(book_id, cover.strip())
            print("Cover updated.")
        elif choice == "6":
            book_id = int(input("Book ID to delete: "))
            service.delete_book(book_id)
            print("Book deleted.")
        elif choice == "7":
            break

def manage_members(service):
    # Similar to manage_books but for members
    while True:
        print("\n--- Manage Members ---")
        print("1. Add Member")
        print("2. List Members")
        print("3. Search Members")
        print("4. Back")
        choice = input("Choose: ").strip()
        if choice == "1":
            name = input("Name: ")
            email = input("Email (optional): ")
            member = service.add_member(name, email)
            print(f"Member added with ID {member.id}")
        elif choice == "2":
            for m in service.get_all_members():
                print(f"ID: {m.id} | {m.name} | {m.email}")
        elif choice == "3":
            term = input("Search term: ")
            for m in service.search_members(term):
                print(f"ID: {m.id} | {m.name} | {m.email}")
        elif choice == "4":
            break

def borrow_book_ui(service):
    print("\nAvailable Books:")
    for b in service.get_all_books():
        if b.available:
            print(f"{b.id}: {b.title}")
    book_id = int(input("Book ID to borrow: "))
    member_id = int(input("Member ID: "))
    loan = service.borrow_book(book_id, member_id)
    print(f"Loan created. Due date: {loan.due_date}")

def return_book_ui(service):
    book_id = int(input("Book ID to return: "))
    service.return_book(book_id)
    print("Book returned.")

if __name__ == "__main__":
    main()