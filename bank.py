import json
import random
import string
from pathlib import Path


class Bank:
    DATABASE = "data.json"

    def __init__(self):
        self.data = self.__load_data()

    def __load_data(self):
        if Path(self.DATABASE).exists():
            with open(self.DATABASE, "r") as f:
                content = f.read().strip()
                return json.loads(content) if content else []
        return []

    def __save_data(self):
        with open(self.DATABASE, "w") as f:
            json.dump(self.data, f, indent=4)

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

    def get_user(self, acc, pin):
        return next((u for u in self.data if u["Account_No"] == acc and u["pin"] == pin), None)

    # ---------- Features ----------
    def create_account(self, name, age, email, pin):
        if age < 18:
            return False, "Must be 18+"

        if not (str(pin).isdigit() and len(str(pin)) == 4):
            return False, "PIN must be 4 digits"

        user = {
            "Name": name,
            "Age": age,
            "Email": email,
            "pin": int(pin),
            "Account_No": self.__generate_account_no(),
            "CustomerId": self.__generate_customer_id(),
            "Balance": 0
        }

        self.data.append(user)
        self.__save_data()
        return True, user

    def deposit(self, acc, pin, amount):
        user = self.get_user(acc, pin)
        if not user:
            return False, "User not found"

        if not (0 < amount <= 50000):
            return False, "Invalid amount"

        user["Balance"] += amount
        self.__save_data()
        return True, "Deposit successful"

    def withdraw(self, acc, pin, amount):
        user = self.get_user(acc, pin)
        if not user:
            return False, "User not found"

        if amount > user["Balance"]:
            return False, "Insufficient balance"

        if not (0 < amount <= 10000):
            return False, "Invalid amount"

        user["Balance"] -= amount
        self.__save_data()
        return True, "Withdrawal successful"

    def update(self, acc, pin, name=None, email=None, new_pin=None):
        user = self.get_user(acc, pin)
        if not user:
            return False, "User not found"

        if name:
            user["Name"] = name
        if email:
            user["Email"] = email
        if new_pin:
            if not (str(new_pin).isdigit() and len(str(new_pin)) == 4):
                return False, "Invalid PIN"
            user["pin"] = int(new_pin)

        self.__save_data()
        return True, "Updated successfully"

    def delete(self, acc, pin):
        user = self.get_user(acc, pin)
        if not user:
            return False, "User not found"

        self.data.remove(user)
        self.__save_data()
        return True, "Deleted successfully"

    def get_details(self, acc, pin):
        user = self.get_user(acc, pin)
        if not user:
            return False, "User not found"
        return True, user