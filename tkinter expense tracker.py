import tkinter as tk
from tkinter import ttk
import csv
import datetime
import os

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.expenses = {}
        self.data_file = "expenses.csv"

        self.load_data()

        self.category_var = tk.StringVar()
        self.amount_var = tk.DoubleVar()

        self.create_widgets()

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

    def add_expense(self):
        category = self.category_var.get()
        amount = self.amount_var.get()

        if not category or not amount:
            return

        timestamp = datetime.datetime.now()
        expense = {'amount': amount, 'timestamp': timestamp}

        if category in self.expenses:
            self.expenses[category].append(expense)
        else:
            self.expenses[category] = [expense]

        self.save_data()
        self.update_expense_list()
        self.category_var.set('')
        self.amount_var.set('')

    def update_expense_list(self):
        for row in self.expense_tree.get_children():
            self.expense_tree.delete(row)

        for category, expenses in self.expenses.items():
            for expense in expenses:
                self.expense_tree.insert('', 'end', values=(category, expense['amount'], expense['timestamp']))

    def create_widgets(self):
        # Category Entry
        category_label = tk.Label(self.root, text="Category:")
        category_label.grid(row=0, column=0, padx=10, pady=10)

        category_entry = ttk.Entry(self.root, textvariable=self.category_var)
        category_entry.grid(row=0, column=1, padx=10, pady=10)

        # Amount Entry
        amount_label = tk.Label(self.root, text="Amount:")
        amount_label.grid(row=1, column=0, padx=10, pady=10)

        amount_entry = ttk.Entry(self.root, textvariable=self.amount_var)
        amount_entry.grid(row=1, column=1, padx=10, pady=10)

        # Add Expense Button
        add_button = ttk.Button(self.root, text="Add Expense", command=self.add_expense)
        add_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Expense Treeview
        columns = ("Category", "Amount", "Timestamp")
        self.expense_tree = ttk.Treeview(self.root, columns=columns, show="headings", height=10)

        for col in columns:
            self.expense_tree.heading(col, text=col)
            self.expense_tree.column(col, width=100)

        self.expense_tree.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        # Load existing expenses
        self.update_expense_list()

# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()
