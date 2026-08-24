from storage.database import Database
from storage.initializer import DatabaseInitializer
from services.expense_service import ExpenseService

def main():
    db = Database("expenses.db")
    db.connect()
    DatabaseInitializer(db).initialize()
    service = ExpenseService(db)

    while True:
        print("\n--- Expense Tracker ---")
        print("1. Manage Categories")
        print("2. Add Expense")
        print("3. View All Expenses")
        print("4. Filter Expenses")
        print("5. Update Expense")
        print("6. Delete Expense")
        print("7. View Summary")
        print("8. Exit")
        choice = input("Choose: ").strip()

        try:
            if choice == "1":
                manage_categories(service)
            elif choice == "2":
                add_expense_ui(service)
            elif choice == "3":
                view_expenses(service.get_all_expenses())
            elif choice == "4":
                filter_expenses_ui(service)
            elif choice == "5":
                update_expense_ui(service)
            elif choice == "6":
                delete_expense_ui(service)
            elif choice == "7":
                show_summary(service)
            elif choice == "8":
                print("Goodbye!")
                break
            else:
                print("Invalid option.")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    db.close()

def manage_categories(service):
    while True:
        print("\n--- Categories ---")
        print("1. Add Category")
        print("2. List Categories")
        print("3. Delete Category")
        print("4. Back")
        choice = input("Choose: ").strip()
        if choice == "1":
            name = input("Category name: ")
            cat = service.add_category(name)
            print(f"Added category with ID {cat.id}")
        elif choice == "2":
            cats = service.get_all_categories()
            for c in cats:
                print(f"{c.id}: {c.name}")
        elif choice == "3":
            cid = int(input("Category ID to delete: "))
            service.delete_category(cid)
            print("Category deleted.")
        elif choice == "4":
            break
        else:
            print("Invalid option.")

def add_expense_ui(service):
    cats = service.get_all_categories()
    if not cats:
        print("No categories. Please add a category first.")
        return
    for c in cats:
        print(f"{c.id}: {c.name}")
    cid = int(input("Category ID: "))
    amount = float(input("Amount: "))
    desc = input("Description (optional): ")
    date_str = input("Date (YYYY-MM-DD, leave blank for today): ")
    if not date_str.strip():
        date_str = None
    exp = service.add_expense(cid, amount, desc, date_str)
    print(f"Expense added with ID {exp.id}")

def view_expenses(expenses):
    if not expenses:
        print("No expenses.")
        return
    print("\nExpenses:")
    for e in expenses:
        print(f"ID: {e.id} | Date: {e.date} | Amount: ${e.amount:.2f} | Desc: {e.description or 'N/A'}")

def filter_expenses_ui(service):
    print("Filter by: 1) Category 2) Date Range")
    choice = input("Choose: ").strip()
    if choice == "1":
        cats = service.get_all_categories()
        for c in cats:
            print(f"{c.id}: {c.name}")
        cid = int(input("Category ID: "))
        expenses = service.get_expenses_by_category(cid)
        view_expenses(expenses)
    elif choice == "2":
        start = input("Start date (YYYY-MM-DD): ")
        end = input("End date (YYYY-MM-DD): ")
        expenses = service.get_expenses_by_date_range(start, end)
        view_expenses(expenses)
    else:
        print("Invalid filter.")

def update_expense_ui(service):
    expense_id = int(input("Expense ID to update: "))
    cats = service.get_all_categories()
    for c in cats:
        print(f"{c.id}: {c.name}")
    cid = int(input("New category ID: "))
    amount = float(input("New amount: "))
    desc = input("New description (optional): ")
    date_str = input("New date (YYYY-MM-DD): ")
    service.update_expense(expense_id, cid, amount, desc, date_str)
    print("Expense updated.")

def delete_expense_ui(service):
    expense_id = int(input("Expense ID to delete: "))
    service.delete_expense(expense_id)
    print("Expense deleted.")

def show_summary(service):
    total = service.total_spent()
    print(f"\nTotal spent: ${total:.2f}")
    by_cat = service.total_by_category()
    print("By category:")
    for cat, amount in by_cat.items():
        print(f"  {cat}: ${amount:.2f}")

if __name__ == "__main__":
    main()