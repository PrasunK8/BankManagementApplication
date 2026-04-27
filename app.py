import streamlit as st
from bank import Bank

bank = Bank()

st.set_page_config(page_title="Bank System", layout="centered")
st.title("🏦 Bank Management System")

menu = st.sidebar.selectbox("Menu", [
    "Create Account",
    "Deposit",
    "Withdraw",
    "Show Details",
    "Update Details",
    "Delete Account"
])

# ---------- Create ----------
if menu == "Create Account":
    st.subheader("Create Account")

    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1)
    email = st.text_input("Email")
    pin = st.text_input("PIN", type="password")

    if st.button("Create"):
        success, result = bank.create_account(name, age, email, pin)

        if success:
            st.success("Account Created!")
            st.info(f"Account No: {result['Account_No']}")
        else:
            st.error(result)

# ---------- Deposit ----------
elif menu == "Deposit":
    st.subheader("Deposit")

    acc = st.number_input("Account No", step=1)
    pin = st.text_input("PIN", type="password")
    amount = st.number_input("Amount", step=1)

    if st.button("Deposit"):
        success, msg = bank.deposit(int(acc), int(pin), amount)

        if success:
            st.success(msg)
        else:
            st.error(msg)

# ---------- Withdraw ----------
elif menu == "Withdraw":
    st.subheader("Withdraw")

    acc = st.number_input("Account No", step=1)
    pin = st.text_input("PIN", type="password")
    amount = st.number_input("Amount", step=1)

    if st.button("Withdraw"):
        success, msg = bank.withdraw(int(acc), int(pin), amount)

        if success:
            st.success(msg)
        else:
            st.error(msg)

# ---------- Show ----------
elif menu == "Show Details":
    st.subheader("Account Details")

    acc = st.number_input("Account No", step=1)
    pin = st.text_input("PIN", type="password")

    if st.button("Show"):
        success, result = bank.get_details(int(acc), int(pin))

        if success:
            st.json(result)
        else:
            st.error(result)

# ---------- Update ----------
elif menu == "Update Details":
    st.subheader("Update Details")

    acc = st.number_input("Account No", step=1)
    pin = st.text_input("PIN", type="password")

    name = st.text_input("New Name")
    email = st.text_input("New Email")
    new_pin = st.text_input("New PIN", type="password")

    if st.button("Update"):
        success, msg = bank.update(
            int(acc),
            int(pin),
            name or None,
            email or None,
            new_pin or None
        )

        if success:
            st.success(msg)
        else:
            st.error(msg)

# ---------- Delete ----------
elif menu == "Delete Account":
    st.subheader("Delete Account")

    acc = st.number_input("Account No", step=1)
    pin = st.text_input("PIN", type="password")

    if st.button("Delete"):
        success, msg = bank.delete(int(acc), int(pin))

        if success:
            st.success(msg)
        else:
            st.error(msg)