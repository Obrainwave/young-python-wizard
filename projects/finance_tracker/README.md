# Personal Finance Tracker

A web application for tracking personal finances. Manage accounts, record income and expenses, organize transactions by category, set monthly budgets, and view rich dashboard summaries. Built with Flask and SQLite, this project follows a clean layered architecture with separated models, services, storage, and web layers.

This project is part of the **Young Python Wizard** Module 9 series.

---

## Features

### Accounts

- ➕ Create accounts of different types: checking, savings, cash, credit.
- 💵 Set initial balances and currency per account.
- 📊 See current balances computed from initial balance plus income minus expenses.
- 🗑️ Delete accounts (with a confirmation that removes associated transactions).

### Transactions

- 💸 Record income and expenses with amount, date, description, account, and category.
- 🏷️ Categorize transactions for detailed reporting.
- ✏️ Edit and delete transactions.
- 🔍 Filter transactions by month, account, category, or type.

### Categories

- 🏷️ Organize transactions into income and expense categories.
- 🎨 Assign a color to each category for visual clarity in lists and charts.
- 🔗 Deleting a category unlinks its transactions (history is preserved) and removes its budgets.

### Budgets

- 💰 Set monthly spending limits for expense categories.
- 📈 Track real-time progress with progress bars showing percent used and remaining amount.
- ⚠️ Visual warnings when approaching or exceeding the budget.

### Dashboard

- 📌 Total balance across all accounts.
- 📆 Current month's total income, total expenses, and net.
- 📊 Budget progress bars for the current month.
- 📋 Recent transactions at a glance.
- 🏦 Quick view of all account balances.

### Reports

- 🔎 Advanced filterable transaction view by month, account, category, or type.
- 🧮 Running totals of income, expenses, and net for the filtered set.

---

## Project Structure

```
finance_tracker/
├── models/
│   ├── __init__.py
│   ├── account.py
│   ├── category.py
│   ├── transaction.py
│   └── budget.py
├── services/
│   ├── __init__.py
│   ├── account_service.py
│   ├── category_service.py
│   ├── transaction_service.py
│   └── budget_service.py
├── storage/
│   ├── __init__.py
│   ├── database.py
│   ├── initializer.py
│   ├── account_repository.py
│   ├── category_repository.py
│   ├── transaction_repository.py
│   └── budget_repository.py
├── webapp/
│   ├── __init__.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── main_routes.py
│   │   ├── account_routes.py
│   │   ├── category_routes.py
│   │   ├── transaction_routes.py
│   │   └── budget_routes.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── accounts.html
│   │   ├── account_form.html
│   │   ├── account_detail.html
│   │   ├── categories.html
│   │   ├── category_form.html
│   │   ├── transactions.html
│   │   ├── transaction_form.html
│   │   ├── budgets.html
│   │   ├── budget_form.html
│   │   └── reports.html
│   └── static/
│       └── style.css
├── main.py
└── requirements.txt
```

- **`models/`** – Data classes (`Account`, `Category`, `Transaction`, `Budget`).
- **`services/`** – Business logic and validation.
- **`storage/`** – Database connection, initialization, and repositories.
- **`webapp/routes/`** – Flask blueprints organized by domain.
- **`webapp/templates/`** – Jinja2 templates.
- **`main.py`** – Entry point that runs the Flask app.

---

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Install dependencies:

```bash
pip install -r requirements.txt
```

### Running the Application

```bash
python main.py
```

Open `http://127.0.0.1:5003` in your browser.

The database (`finance.db`) and tables are created automatically on the first run.

---

## Usage

### First Steps

1. **Create an account** (e.g., "Main Checking" with an initial balance of $1000).
2. **Create categories** – at least one income category (e.g., "Salary") and a few expense categories (e.g., "Groceries", "Rent", "Entertainment").
3. **Add transactions** – link each transaction to an account and (optionally) a category. The type must match the category type.
4. **Set budgets** – go to the Budgets page, select an expense category and a month, and enter a limit.

### Navigation

- **Dashboard** (`/`): overview of balances, monthly summary, budgets, and recent activity.
- **Accounts** (`/accounts`): manage accounts and see balances.
- **Transactions** (`/transactions`): add, edit, filter transactions.
- **Categories** (`/categories`): manage income and expense categories.
- **Budgets** (`/budgets`): set and track monthly budgets.
- **Reports** (`/reports`): advanced filtering with running totals.

---

## How It Works

### Database Schema

The SQLite database contains four tables with foreign-key relationships:

- **accounts** – name, type, initial balance, currency.
- **categories** – name, type (income/expense), color.
- **transactions** – account_id, category_id (nullable), type, amount, description, date.
- **budgets** – category_id, month (YYYY-MM), amount; unique on `(category_id, month)`.

### Layered Architecture

- **Repositories** (in `storage/`) handle all SQL. Each method opens its own connection, making the app safe under Flask's multi-threaded dev server.
- **Services** (in `services/`) contain business logic: validation, aggregation across repositories, balance calculations, and budget progress.
- **Models** (in `models/`) are simple data containers.
- **Routes** (in `webapp/routes/`) are split into five blueprints, one per domain, for clarity and maintainability.

### Balances and Aggregations

Balances are never stored. They are computed on demand:

```
balance = initial_balance + SUM(income) - SUM(expense)
```

The `TransactionRepository` provides aggregation methods (`sum_by_account`, `sum_for_month`, `sum_expense_by_category`) that compute totals in a single SQL query using `CASE WHEN`. This keeps the service layer clean and fast.

### Validation

The service layer enforces:

- Non-empty names.
- Valid account and category types.
- Positive amounts.
- Date format `YYYY-MM-DD`.
- Category type must match transaction type.
- Budgets only for expense categories.
- Positive budget amounts.

This centralizes business rules and prevents invalid data from reaching the database.

### Budget Progress

Budgets are stored per (category, month). The dashboard and budgets page combine the stored limit with live spending from `TransactionRepository.sum_expense_by_category`, computing:

- Amount spent
- Amount remaining
- Percent used (with color-coded progress bar)

---

## Extending the Project

Here are ideas to enhance the app:

- **Transfers** between accounts (creates paired transactions).
- **Recurring transactions** (salary, rent) applied to a month.
- **Currency conversion** for multi-currency portfolios.
- **Charts** using Chart.js (via CDN) for spending trends.
- **CSV import/export** of transactions.
- **Budget alerts** highlighting over-budget categories.
- **Authentication** with per-user data (add `user_id` columns and session login).
- **Pagination** on the transactions page.

---

## License

This project is part of the **Young Python Wizard** learning repository and is free to use for personal and educational purposes.

Happy tracking! 💰🐍