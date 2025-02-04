import argparse
import json
import os
from datetime import datetime

# File to store expenses
EXPENSE_FILE = "expenses.json"

# Load expenses from file
def load_expenses():
    if os.path.exists(EXPENSE_FILE):
        try:
            with open(EXPENSE_FILE, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            # If the file is empty or contains invalid JSON, return an empty list
            return []
    return []

# def load_expenses():
#     if os.path.exists(EXPENSE_FILE):
#         with open(EXPENSE_FILE, "r") as file:
#             return json.load(file)
#     return []

# Save expenses to file
def save_expenses(expenses):
    with open(EXPENSE_FILE, "w") as file:
        json.dump(expenses, file, indent=4)

# Generate a unique ID for a new expense
def generate_id(expenses):
    return max([expense["id"] for expense in expenses], default=0) + 1

# Add an expense
def add_expense(args):
    if args.amount < 0:
        print("Error: Amount cannot be negative.")
        return
    expenses = load_expenses()
    expense = {
        "id": generate_id(expenses),
        "date": datetime.now().strftime("%Y-%m-%d"),
        "description": args.description,
        "amount": args.amount
    }
    expenses.append(expense)
    save_expenses(expenses)
    print(f"Expense added successfully (ID: {expense['id']})")

# def add_expense(args):
#     expenses = load_expenses()
#     expense = {
#         "id": generate_id(expenses),
#         "date": datetime.now().strftime("%Y-%m-%d"),
#         "description": args.description,
#         "amount": args.amount
#     }
#     expenses.append(expense)
#     save_expenses(expenses)
#     print(f"Expense added successfully (ID: {expense['id']})")

# List all expenses
def list_expenses(args):
    expenses = load_expenses()
    if not expenses:
        print("No expenses found.")
        return

    print("ID  Date       Description  Amount")
    for expense in expenses:
        print(f"{expense['id']}   {expense['date']}  {expense['description']}        ${expense['amount']}")

# Delete an expense

def delete_expense(args):
    expenses = load_expenses()
    initial_length = len(expenses)
    expenses = [expense for expense in expenses if expense["id"] != args.id]
    if len(expenses) == initial_length:
        print(f"No expense found with ID: {args.id}")
    else:
        save_expenses(expenses)
        print(f"Expense deleted successfully (ID: {args.id})")
# def delete_expense(args):
#     expenses = load_expenses()
#     expenses = [expense for expense in expenses if expense["id"] != args.id]
#     save_expenses(expenses)
#     print(f"Expense deleted successfully (ID: {args.id})")

#the summary function below handle both cases: 
# 1) displaying the total summary of all expenses 
# 2) the summary for a specific month based on whether the --month argument is provided.
def summary(args):
    expenses = load_expenses()
    
    if args.month:
        # Filter expenses for the specified month
        month_expenses = [
            expense for expense in expenses
            if datetime.strptime(expense["date"], "%Y-%m-%d").month == args.month
        ]
        total = sum(expense["amount"] for expense in month_expenses)
        print(f"Total expenses for {datetime.strftime(datetime.now().replace(month=args.month), '%B')}: ${total:.2f}")
    else:
        # Calculate total expenses for all months
        total = sum(expense["amount"] for expense in expenses)
        print(f"Total expenses: ${total:.2f}")




# View a summary of all expenses
# def summary(args):
#     expenses = load_expenses()
#     total = sum(expense["amount"] for expense in expenses)
#     print(f"Total expenses: ${total:.2f}")

# # View a summary of expenses for a specific month
# def summary_month(args):
#     expenses = load_expenses()
#     month_expenses = [
#         expense for expense in expenses
#         if datetime.strptime(expense["date"], "%Y-%m-%d").month == args.month
#     ]
#     total = sum(expense["amount"] for expense in month_expenses)
#     print(f"Total expenses for {datetime.strftime(datetime.now().replace(month=args.month), '%B')}: ${total:.2f}")

# Main function to handle command-line arguments
def main():
    parser = argparse.ArgumentParser(description="Expense Tracker")
    subparsers = parser.add_subparsers(dest="command")

    # Add expense command
    add_parser = subparsers.add_parser("add", help="Add an expense")
    add_parser.add_argument("--description", required=True, help="Description of the expense")
    add_parser.add_argument("--amount", type=float, required=True, help="Amount of the expense")
    add_parser.set_defaults(func=add_expense)

    # List expenses command
    list_parser = subparsers.add_parser("list", help="List all expenses")
    list_parser.set_defaults(func=list_expenses)

    # Delete expense command
    delete_parser = subparsers.add_parser("delete", help="Delete an expense")
    delete_parser.add_argument("--id", type=int, required=True, help="ID of the expense to delete")
    delete_parser.set_defaults(func=delete_expense)
   
   # Summary command (handles both cases)
    summary_parser = subparsers.add_parser("summary", help="View a summary of all expenses or for a specific month")
    summary_parser.add_argument("--month", type=int, help="Month (1-12) to filter expenses")
    summary_parser.set_defaults(func=summary)

    # # Summary command
    # summary_parser = subparsers.add_parser("summary", help="View a summary of all expenses")
    # summary_parser.set_defaults(func=summary)

    # # Summary for a specific month
    # summary_month_parser = subparsers.add_parser("summary-month", help="View a summary of expenses for a specific month")
    # summary_month_parser.add_argument("--month", type=int, required=True, help="Month (1-12)")
    # summary_month_parser.set_defaults(func=summary_month)

    args = parser.parse_args()
    if args.command:
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()