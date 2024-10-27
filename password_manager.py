import streamlit as st
from cryptography.fernet import Fernet
import csv

# Load encryption key
def load_key():
    return open("secret.key", "rb").read()

# Encrypt and decrypt passwords
def encrypt_password(password):
    return Fernet(load_key()).encrypt(password.encode()).decode()

def decrypt_password(encrypted_password):
    try:
        return Fernet(load_key()).decrypt(encrypted_password.encode()).decode()
    except Exception as e:
        print(f"Error decrypting password: {e}")
        return None

# Save password to CSV
def save_password(service, username, password):
    encrypted_password = encrypt_password(password)
    with open("passwords.csv", "a", newline='') as file:
        writer = csv.writer(file)
        writer.writerow([service, username, encrypted_password])

# Retrieve password from CSV
def get_password(service):
    with open("passwords.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == service:
                return row[1], decrypt_password(row[2])
    return None, None

# Streamlit UI
st.title("Password Manager")

menu = st.sidebar.selectbox("Menu", ["Add Password", "Get Password"])

if menu == "Add Password":
    service = st.text_input("Service Name")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Save"):
        save_password(service, username, password)
        st.success("Password saved!")

elif menu == "Get Password":
    service = st.text_input("Service Name")
    if st.button("Retrieve"):
        username, password = get_password(service)
        if username:
            st.write(f"**Username:** {username}")
            st.write(f"**Password:** {password}")
        else:
            st.error("Service not found.")
