import csv
import datetime
import os

class ExpenseTracker:
    def __init__(self):
        self.expenses = {}
        self.data_file = "expenses.csv"
        self.load_data()

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    category = row['Category']
                    amount = float(row['Amount'])
                    timestamp = datetime.datetime.strptime(row['Timestamp'], '%Y-%m-%d %H:%M:%S.%f')
                    
                    expense = {'amount': amount, 'timestamp': timestamp}
                    
                    if category in self.expenses:
                        self.expenses[category].append(expense)
                    else:
                        self.expenses[category] = [expense]

    def save_data(self):
        with open(self.data_file, 'w', newline='') as file:
            fieldnames = ['Category', 'Amount', 'Timestamp']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            for category, expenses in self.expenses.items():
                for expense in expenses:
                    writer.writerow({
                        'Category': category,
                        'Amount': expense['amount'],
                        'Timestamp': expense['timestamp']
                    })

    def add_expense(self, category, amount):
        timestamp = datetime.datetime.now()
        expense = {'amount': amount, 'timestamp': timestamp}

        if category in self.expenses:
            self.expenses[category].append(expense)
        else:
            self.expenses[category] = [expense]

        self.save_data()
        print("Expense added successfully!")

    def view_expenses(self):
        for category, expenses in self.expenses.items():
            print(f"\nCategory: {category}")
            for expense in expenses:
                print(f"Amount: ${expense['amount']} | Date: {expense['timestamp']}")

    def total_expenses(self):
        total = 0
        for expenses in self.expenses.values():
            total += sum(expense['amount'] for expense in expenses)
        return total

# Example usage
if __name__ == "__main__":
    tracker = ExpenseTracker()

    while True:
        print("\nExpense Tracker Menu:")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. View Total Expenses")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ")

        try:
            if choice == '1':
                category = input("Enter expense category: ")
                amount = float(input("Enter expense amount: "))
                tracker.add_expense(category, amount)

            elif choice == '2':
                tracker.view_expenses()

            elif choice == '3':
                total = tracker.total_expenses()
                print(f"\nTotal Expenses: rs{total}")

            elif choice == '4':
                print("Exiting Expense Tracker. Goodbye!")
                break

            else:
                print("Invalid choice. Please enter a number between 1 and 4.")

        except ValueError:
            print("Invalid input. Please enter a valid number.")
        except Exception as e:
            print(f"An error occurred: {e}")
