# Bank Management System (Optimized Version)

import json
import random
import string
from pathlib import Path


class Bank:
    DATABASE = "data.json"

    def __init__(self):
        self.data = self.__load_data()

    # ---------- File Handling ----------
    def __load_data(self):
        try:
            if Path(self.DATABASE).exists():
                with open(self.DATABASE, "r") as f:
                    content = f.read().strip()
                    return json.loads(content) if content else []
            return []
        except Exception as e:
            print(f"Error loading data: {e}")
            return []

    def __save_data(self):
        with open(self.DATABASE, "w") as f:
            json.dump(self.data, f, indent=4)

    # ---------- Utility Methods ----------
    def __generate_account_no(self):
        existing = {user["Account_No"] for user in self.data}
        while True:
            acc = random.randint(10**9, 10**10 - 1)
            if acc not in existing:
                return acc

    def __generate_customer_id(self):
        chars = random.choices(string.ascii_letters, k=3)
        nums = random.choices(string.digits, k=4)
        sp = random.choice("!@#$&")
        temp = chars + nums + [sp]
        random.shuffle(temp)
        return "".join(temp)

    def __get_user(self, acc, pin):
        return next((u for u in self.data if u["Account_No"] == acc and u["pin"] == pin), None)

    # ---------- Core Features ----------
    def create_account(self):
        try:
            age = int(input("Enter age: "))
            pin = input("Enter 4-digit PIN: ")

            if age < 18:
                print("Must be 18+ to open account.")
                return

            if not (pin.isdigit() and len(pin) == 4):
                print("PIN must be exactly 4 digits.")
                return

            user = {
                "Name": input("Enter name: "),
                "Age": age,
                "Email": input("Enter email: "),
                "pin": int(pin),
                "Account_No": self.__generate_account_no(),
                "CustomerId": self.__generate_customer_id(),
                "Balance": 0
            }

            self.data.append(user)
            self.__save_data()

            print("\n✅ Account Created Successfully!")
            print(f"Account Number: {user['Account_No']}")

        except ValueError:
            print("Invalid input!")

    def deposit_money(self):
        try:
            acc = int(input("Enter account number: "))
            pin = int(input("Enter PIN: "))
            user = self.__get_user(acc, pin)

            if not user:
                print("User not found!")
                return

            amount = int(input("Enter amount to deposit: "))

            if 0 < amount <= 50000:
                user["Balance"] += amount
                self.__save_data()
                print("✅ Deposit successful!")
            else:
                print("Amount must be between 1 and 50000")

        except ValueError:
            print("Invalid input!")

    def withdraw_money(self):
        try:
            acc = int(input("Enter account number: "))
            pin = int(input("Enter PIN: "))
            user = self.__get_user(acc, pin)

            if not user:
                print("User not found!")
                return

            amount = int(input("Enter amount to withdraw: "))

            if amount <= 0 or amount > 10000:
                print("Withdraw limit is 1 to 10000")
            elif user["Balance"] < amount:
                print("Insufficient balance!")
            else:
                user["Balance"] -= amount
                self.__save_data()
                print("✅ Withdrawal successful!")

        except ValueError:
            print("Invalid input!")

    def show_details(self):
        try:
            acc = int(input("Enter account number: "))
            pin = int(input("Enter PIN: "))
            user = self.__get_user(acc, pin)

            if not user:
                print("User not found!")
                return

            print("\n--- Account Details ---")
            for k, v in user.items():
                print(f"{k}: {v}")

        except ValueError:
            print("Invalid input!")

    def update_details(self):
        try:
            acc = int(input("Enter account number: "))
            pin = int(input("Enter PIN: "))
            user = self.__get_user(acc, pin)

            if not user:
                print("User not found!")
                return

            print("\nLeave blank to keep old value")

            name = input("New name: ") or user["Name"]
            email = input("New email: ") or user["Email"]
            new_pin = input("New PIN: ")

            if new_pin:
                if not (new_pin.isdigit() and len(new_pin) == 4):
                    print("Invalid PIN format!")
                    return
                user["pin"] = int(new_pin)

            user["Name"] = name
            user["Email"] = email

            self.__save_data()
            print("✅ Details updated!")

        except ValueError:
            print("Invalid input!")

    def delete_account(self):
        try:
            acc = int(input("Enter account number: "))
            pin = int(input("Enter PIN: "))
            user = self.__get_user(acc, pin)

            if not user:
                print("User not found!")
                return

            confirm = input("Confirm delete (Y/N): ").upper()
            if confirm == "Y":
                self.data.remove(user)
                self.__save_data()
                print("✅ Account deleted!")
            else:
                print("Cancelled.")

        except ValueError:
            print("Invalid input!")


# ---------- Main Menu ----------
def main():
    bank = Bank()

    while True:
        print("""
====== BANK MENU ======
1. Create Account
2. Deposit Money
3. Withdraw Money
4. Show Details
5. Update Details
6. Delete Account
7. Exit
""")

        try:
            choice = int(input("Enter choice: "))

            if choice == 1:
                bank.create_account()
            elif choice == 2:
                bank.deposit_money()
            elif choice == 3:
                bank.withdraw_money()
            elif choice == 4:
                bank.show_details()
            elif choice == 5:
                bank.update_details()
            elif choice == 6:
                bank.delete_account()
            elif choice == 7:
                print("Exiting... 👋")
                break
            else:
                print("Invalid choice!")

        except ValueError:
            print("Please enter a valid number!")


if __name__ == "__main__":
    main()