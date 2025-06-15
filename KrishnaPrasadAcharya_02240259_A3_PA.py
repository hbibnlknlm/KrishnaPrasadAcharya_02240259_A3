
import random
import os
import tkinter as tk
from tkinter import messagebox
import tkinter.simpledialog as simpledialog


class InvalidInputException(Exception):
    """Raised when the user inputs an invalid value."""
    pass

class InsufficientFundsException(Exception):
    """Raised when an account has insufficient funds for a transaction."""
    pass

class AccountNotFoundException(Exception):
    """Raised when a requested account does not exist."""
    pass

class BankAccount:
    def __init__(self, account_number, password, account_type, balance=0):
        """Initializes a bank account."""
        self.account_number = account_number
        self.password = password
        self.account_type = account_type
        self.balance = float(balance)

    def deposit(self, amount):
        """Deposits the specified amount to the account."""
        if amount <= 0:
            raise InvalidInputException("Deposit amount must be positive.")
        self.balance += amount

    def withdraw(self, amount):
        """Withdraws the specified amount if funds are sufficient."""
        if amount <= 0:
            raise InvalidInputException("Withdrawal amount must be positive.")
        if self.balance < amount:
            raise InsufficientFundsException("Insufficient balance.")
        self.balance -= amount

    def transfer(self, amount, recipient_account):
        """Transfers funds to another account."""
        self.withdraw(amount)
        recipient_account.deposit(amount)

class PersonalAccount(BankAccount):
    def __init__(self, account_number, password, balance=0):
        super().__init__(account_number, password, "Personal", balance)

class BusinessAccount(BankAccount):
    def __init__(self, account_number, password, balance=0):
        super().__init__(account_number, password, "Business", balance)

class BankingSystem:
    def __init__(self):
        self.accounts = {}
        self.load_accounts()

    def load_accounts(self):
        """Loads account data from the file into memory."""
        if os.path.exists("accounts.txt"):
            with open("accounts.txt", "r") as f:
                for line in f:
                    acc_no, pwd, acc_type, balance = line.strip().split(',')
                    if acc_type == "Personal":
                        self.accounts[acc_no] = PersonalAccount(acc_no, pwd, float(balance))
                    elif acc_type == "Business":
                        self.accounts[acc_no] = BusinessAccount(acc_no, pwd, float(balance))

    def save_accounts(self):
        """Saves the current account data back to the file."""
        with open("accounts.txt", "w") as f:
            for acc in self.accounts.values():
                f.write(f"{acc.account_number},{acc.password},{acc.account_type},{acc.balance}\n")

    def create_account(self, acc_type):
        """Creates a new personal or business account."""
        acc_no = str(random.randint(10000, 99999))
        pwd = str(random.randint(1000, 9999))
        if acc_type == "Personal":
            acc = PersonalAccount(acc_no, pwd)
        else:
            acc = BusinessAccount(acc_no, pwd)
        self.accounts[acc_no] = acc
        self.save_accounts()
        return acc_no, pwd

    def login(self, acc_no, pwd):
        """Authenticates a user based on account number and password."""
        acc = self.accounts.get(acc_no)
        if not acc or acc.password != pwd:
            raise InvalidInputException("Invalid login credentials.")
        return acc

    def delete_account(self, acc_no):
        """Deletes a user account."""
        if acc_no in self.accounts:
            del self.accounts[acc_no]
            self.save_accounts()

    def top_up_mobile(self, acc, number, amount):
        """Tops up a mobile number with given amount."""
        if len(number) != 10 or not number.isdigit():
            raise InvalidInputException("Invalid phone number.")
        acc.withdraw(amount)
        return f"Successfully topped up ₹{amount} to {number}."

def processUserInput(choice, system, current_account):
    """Handles user menu input."""
    if choice == "1":
        acc_type = input("Enter Account Type (Personal/Business): ").capitalize()
        acc_no, pwd = system.create_account(acc_type)
        print(f"Account created. Number: {acc_no}, Password: {pwd}")
    elif choice == "2":
        acc_no = input("Account Number: ")
        pwd = input("Password: ")
        current_account = system.login(acc_no, pwd)
        print(f"Logged in as {acc_no}")
    elif choice == "3" and current_account:
        print(f"Balance: ₹{current_account.balance}")
    elif choice == "4" and current_account:
        amt = float(input("Enter amount to deposit: "))
        current_account.deposit(amt)
        system.save_accounts()
    elif choice == "5" and current_account:
        amt = float(input("Enter amount to withdraw: "))
        current_account.withdraw(amt)
        system.save_accounts()
    elif choice == "6" and current_account:
        target_acc = input("Enter target account: ")
        amt = float(input("Enter amount to transfer: "))
        if target_acc not in system.accounts:
            raise AccountNotFoundException("Recipient account not found.")
        current_account.transfer(amt, system.accounts[target_acc])
        system.save_accounts()
    elif choice == "7" and current_account:
        number = input("Enter 10-digit mobile number: ")
        amt = float(input("Enter amount to top up: "))
        print(system.top_up_mobile(current_account, number, amt))
        system.save_accounts()
    elif choice == "8" and current_account:
        system.delete_account(current_account.account_number)
        print("Account deleted.")
        current_account = None
    elif choice == "9":
        print("Goodbye!")
        exit()
    else:
        raise InvalidInputException("Invalid choice or not logged in.")
    return current_account

class BankingGUI:
    def __init__(self, system):
        self.system = system
        self.current_account = None
        self.root = tk.Tk()
        self.root.title("Banking System GUI")
        self.root.geometry("600x400") 

        self.label = tk.Label(self.root, text="Welcome to GUI Banking System")
        self.label.pack()

        tk.Button(self.root, text="Open Account", command=self.open_account).pack()
        tk.Button(self.root, text="Login", command=self.login).pack()
        tk.Button(self.root, text="Check Balance", command=self.check_balance).pack()
        tk.Button(self.root, text="Top Up Mobile", command=self.top_up_mobile).pack()

    def run(self):
        self.root.mainloop()

    def open_account(self):
        acc_type = simpledialog.askstring("Input", "Enter Account Type (Personal/Business):")
        if acc_type:
            acc_no, pwd = self.system.create_account(acc_type.capitalize())
            messagebox.showinfo("Success", f"Account: {acc_no}\nPassword: {pwd}")

    def login(self):
        acc_no = simpledialog.askstring("Input", "Enter Account Number:")
        pwd = simpledialog.askstring("Input", "Enter Password:")
        try:
            self.current_account = self.system.login(acc_no, pwd)
            messagebox.showinfo("Login", f"Logged in as {acc_no}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def check_balance(self):
        if self.current_account:
            messagebox.showinfo("Balance", f"Balance: ₹{self.current_account.balance}")
        else:
            messagebox.showerror("Error", "Login first.")

    def top_up_mobile(self):
        if self.current_account:
            number = simpledialog.askstring("Top Up", "Enter 10-digit mobile number:")
            amount = simpledialog.askfloat("Top Up", "Enter amount:")
            try:
                msg = self.system.top_up_mobile(self.current_account, number, amount)
                messagebox.showinfo("Success", msg)
                self.system.save_accounts()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showerror("Error", "Login first.")

def main():
    system = BankingSystem()
    gui = BankingGUI(system)
    gui.run()

if __name__ == "__main__":
    main()
