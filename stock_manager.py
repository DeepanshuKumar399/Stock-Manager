import tkinter as tk
from tkinter import *
from tkinter import messagebox, simpledialog
import pandas as pd


# Initialize the main application window
root = tk.Tk()
root.title("Stock Management System - Teams-Corporations")
root.geometry('350x500')
root.configure(background='#E7D4B5', highlightbackground='#E7D4B5', highlightcolor='#E7D4B5')



# Functions for handling user actions
def login():
    log_dat1 = simpledialog.askstring("Login", "Enter the name:")
    log_dat2 = simpledialog.askstring("Login", "Enter the password:", show='*')
    with open('stock_user_data', 'r') as f:
        a = f.readlines()
        user_found = False
        for line in a:
            if f"Name : {log_dat1} & Password : {log_dat2}" in line:
                user_found = True
                break
        if user_found:
            messagebox.showinfo("Login", f"Welcome back {log_dat1}!")
            stock_management()
        else:
            messagebox.showerror("Login", "Invalid user info, please try again!")


def signup():
    sign_dat1 = simpledialog.askstring("Signup", "Please enter your name:")
    while True:
        sign_dat2 = simpledialog.askstring("Signup", "Password (numeric only):", show='*')
        if sign_dat2.isdigit():
            break
        else:
            messagebox.showerror("Signup", "Please enter a numeric value only!")
    
    with open('stock_user_data', 'a') as f:
        f.write(f"Name : {sign_dat1} & Password : {sign_dat2}\n")
    messagebox.showinfo("Signup", "Your account has been successfully created!")

def stock_management():
    def add_stock():
        data = {"Name": [], "Number": [], "Current Rate": [], "Amount": []}
        while True:
            new_stock = simpledialog.askstring("Add Stock", "Enter the name of the stock (or 'done' to finish):")
            if new_stock.lower() == 'done':
                break
            number_of_stocks = simpledialog.askinteger("Add Stock", "Enter the number of stocks purchased:")
            current_value = simpledialog.askinteger("Add Stock", "Enter the current rate of one stock:")
            amount = number_of_stocks * current_value
            data["Name"].append(new_stock.upper())
            data["Number"].append(number_of_stocks)
            data["Current Rate"].append(current_value)
            data["Amount"].append(amount)
        df = pd.DataFrame(data)
        df.to_csv('stocks.csv', mode='a', header=False, index=False)
        messagebox.showinfo("Add Stock", "New stocks have been successfully added!")

    def update_stock():
        df = pd.read_csv('stocks.csv')
        upd_stock = simpledialog.askstring("Update Stock", "Enter the name of the stock:")
        upper_case_upd_name = upd_stock.upper()
        result = df.isin([upper_case_upd_name])
        found_position = result[result.any(axis=1)]
        if not found_position.empty:
            for index, row in found_position.iterrows():
                columns_with_value = row[row].index.tolist()
                for column in columns_with_value:
                    upd_amount = simpledialog.askinteger("Update Stock", "Enter the new number of stocks purchased:")
                    upd_rate = simpledialog.askinteger("Update Stock", "Enter the new current rate of one stock:")
                    number_of_stocks = df.loc[index, 'Number']
                    current_value = df.loc[index, 'Current Rate']
                    amount = int(current_value) * int(number_of_stocks)
                    upd_amount_value = amount + (upd_amount * upd_rate)
                    df.loc[index, 'Number'] = int(number_of_stocks) + int(upd_amount)
                    df.loc[index, 'Current Rate'] = upd_rate
                    df.loc[index, 'Amount'] = upd_amount_value
                    df.to_csv('stocks.csv', mode='w', index=False)
                    messagebox.showinfo("Update Stock", f"The stock data for {upper_case_upd_name} has been successfully updated!")
        else:
            messagebox.showerror("Update Stock", "No stock found for such name!")

    def view_total_investment():
        df = pd.read_csv('stocks.csv')
        total = df['Amount'].sum()
        messagebox.showinfo("Total Investment", f"The total amount of the holding is {total}")

    stock_window = tk.Toplevel(root)
    stock_window.title("Stock Management")

    tk.Button(stock_window, text="Add a new stock", command=add_stock).pack(pady=5)
    tk.Button(stock_window, text="Update the current holding", command=update_stock).pack(pady=5)
    tk.Button(stock_window, text="Check the sum of entire investments in the portfolio", command=view_total_investment).pack(pady=5)
    tk.Button(stock_window, text="Exit", command=stock_window.destroy).pack(pady=5)

# Main menu buttons
tk.Button(root, text="Login", command=login, width=30).pack(pady=10)
tk.Button(root, text="Signup", command=signup,width=30).pack(pady=10)
tk.Button(root, text="Exit", command=root.quit, width=30).pack(pady=10)

# Run the application
root.mainloop()
