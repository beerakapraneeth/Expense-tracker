import os
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.simpledialog import askstring
import matplotlib.pyplot as plt
from collections import defaultdict

def add_expense():
    date = date_entry.get()
    category = category_entry.get()
    amount = amount_entry.get()

    if date and category and amount:
        year, month, day = date.split("-")
        with open("expenses.txt", "a") as file:
            file.write(f"{year},{month},{day},{category},{amount}\n")
        status_label.config(text="Expense added successfully!", fg="green")
        date_entry.delete(0, tk.END)
        category_entry.delete(0, tk.END)
        amount_entry.delete(0, tk.END)
        view_expenses()
    else:
        status_label.config(text="Please fill all the fields!", fg="red")


def delete_expense():
    selected_item = expenses_tree.selection()
    if selected_item:
        item_text = expenses_tree.item(selected_item, "values")
        date, category, amount = item_text
        with open("expenses.txt", "r") as file:
            lines = file.readlines()
        with open("expenses.txt", "w") as file:
            for line in lines:
                if line.strip() != f"{date},{category},{amount}":
                    file.write(line)
        status_label.config(text="Expense deleted successfully!", fg="green")
        view_expenses()
    else:
        status_label.config(text="Please select an expense to delete!", fg="red")

def view_expenses():
    if os.path.exists("expenses.txt"):
        total_expense = 0
        expenses_tree.delete(*expenses_tree.get_children())
        with open("expenses.txt", "r") as file:
            for line in file:
                year, month, day, category, amount = line.strip().split(",")
                date = f"{year}-{month}-{day}"
                expenses_tree.insert("", tk.END, values=(date, category, amount))
                total_expense += float(amount)
        total_label.config(text=f"Total Expense: {total_expense:.2f}")
    else:
        total_label.config(text="No expenses recorded.")
        expenses_tree.delete(*expenses_tree.get_children())


def view_yearly_expenses():
    year = askstring("Yearly Expenses", "Enter the year (YYYY):")
    if year:
        expenses_by_category = defaultdict(float)
        with open("expenses.txt", "r") as file:
            for line in file:
                line_year, month, day, category, amount = line.strip().split(",")
                if line_year == year:
                    expenses_by_category[category] += float(amount)

        if expenses_by_category:
            plt.figure(figsize=(8, 6))

            def autopct_format(values):
                def my_format(pct):
                    total = sum(values)
                    val = pct * total / 100.0
                    return f'{pct:.1f}%\n({val:.2f})'
                return my_format

            plt.pie(expenses_by_category.values(), labels=expenses_by_category.keys(),
                    autopct=autopct_format(list(expenses_by_category.values())), startangle=140)
            plt.title(f"Expenses for {year}")
            plt.show()
        else:
            messagebox.showinfo("Yearly Expenses", f"No expenses found for the year {year}.")

def view_monthly_expenses():
    year_month = askstring("Monthly Expenses", "Enter the year and month (YYYY-MM):")
    if year_month:
        year, month = year_month.split("-")
        expenses_by_category = defaultdict(float)
        with open("expenses.txt", "r") as file:
            for line in file:
                line_year, line_month, day, category, amount = line.strip().split(",")
                if line_year == year and line_month == month:
                    expenses_by_category[category] += float(amount)

        if expenses_by_category:
            plt.figure(figsize=(8, 6))

            def autopct_format(values):
                def my_format(pct):
                    total = sum(values)
                    val = pct * total / 100.0
                    return f'{pct:.1f}%\n({val:.2f})'
                return my_format

            plt.pie(expenses_by_category.values(), labels=expenses_by_category.keys(),
                    autopct=autopct_format(list(expenses_by_category.values())), startangle=140)
            plt.title(f"Expenses for {year_month}")
            plt.show()
        else:
            messagebox.showinfo("Monthly Expenses", f"No expenses found for {year_month}.")


def view_custom_expenses():
    start_date = askstring("Custom Date Range", "Enter the start date (YYYY-MM-DD):")
    end_date = askstring("Custom Date Range", "Enter the end date (YYYY-MM-DD):")

    if start_date and end_date:
        expenses_by_category = defaultdict(float)
        with open("expenses.txt", "r") as file:
            for line in file:
                year, month, day, category, amount = line.strip().split(",")
                date = f"{year}-{month}-{day}"
                if start_date <= date <= end_date:
                    expenses_by_category[category] += float(amount)

        if expenses_by_category:
            plt.figure(figsize=(8, 6))

            def autopct_format(values):
                def my_format(pct):
                    total = sum(values)
                    val = pct * total / 100.0
                    return f'{pct:.1f}%\n({val:.2f})'

                return my_format

            plt.pie(expenses_by_category.values(), labels=expenses_by_category.keys(),
                    autopct=autopct_format(list(expenses_by_category.values())), startangle=140)
            plt.title(f"Expenses from {start_date} to {end_date}")
            plt.show()
        else:
            messagebox.showinfo("Custom Date Range Analysis", f"No expenses found between {start_date} and {end_date}.")



# Create the main application window
root = tk.Tk()
root.title("Expense Tracker")

# Create labels and entries for adding expenses
date_label = tk.Label(root, text="Date (YYYY-MM-DD):")
date_label.grid(row=0, column=0, padx=5, pady=5)
date_entry = tk.Entry(root)
date_entry.grid(row=0, column=1, padx=5, pady=5)

category_label = tk.Label(root, text="Category:")
category_label.grid(row=1, column=0, padx=5, pady=5)
category_entry = tk.Entry(root)
category_entry.grid(row=1, column=1, padx=5, pady=5)

amount_label = tk.Label(root, text="Amount:")
amount_label.grid(row=2, column=0, padx=5, pady=5)
amount_entry = tk.Entry(root)
amount_entry.grid(row=2, column=1, padx=5, pady=5)

add_button = tk.Button(root, text="Add Expense", command=add_expense)
add_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

# Create a treeview to display expenses
columns = ("Date", "Category", "Amount")
expenses_tree = ttk.Treeview(root, columns=columns, show="headings")
expenses_tree.heading("Date", text="Date")
expenses_tree.heading("Category", text="Category")
expenses_tree.heading("Amount", text="Amount")
expenses_tree.grid(row=4, column=0, columnspan=3, padx=5, pady=5)

# Create a label to display the total expense
total_label = tk.Label(root, text="")
total_label.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

# Create a label to show the status of expense addition and deletion
status_label = tk.Label(root, text="", fg="green")
status_label.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

# Create buttons to view, delete, and analyze expenses
view_button = tk.Button(root, text="View Expenses", command=view_expenses)
view_button.grid(row=7, column=0, padx=5, pady=10)

delete_button = tk.Button(root, text="Delete Expense", command=delete_expense)
delete_button.grid(row=7, column=1, padx=5, pady=10)

yearly_button = tk.Button(root, text="Yearly Expenses", command=view_yearly_expenses)
yearly_button.grid(row=8, column=0, padx=5, pady=10)

monthly_button = tk.Button(root, text="Monthly Expenses", command=view_monthly_expenses)
monthly_button.grid(row=8, column=1, padx=5, pady=10)

custom_button = tk.Button(root, text="Custom Date Range Analysis", command=view_custom_expenses)
custom_button.grid(row=9, column=0, columnspan=2, padx=5, pady=10)


# Check if the 'expenses.txt' file exists; create it if it doesn't
if not os.path.exists("expenses.txt"):
    with open("expenses.txt", "w"):
        pass

# Display existing expenses on application start
view_expenses()

root.mainloop()
