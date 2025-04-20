import streamlit as st
import json
import os
import base64
import time
from cryptography.fernet import Fernet
from hashlib import pbkdf2_hmac

# --------------------------- Constants & Globals ----------------------------

DATA_FILE = "secure_data.json"
LOGIN_CREDENTIALS = {"admin": "admin123"}  # Simple predefined login
LOCKOUT_TIME = 60  # seconds

# Load data
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        stored_data = json.load(f)
else:
    stored_data = {}

# --------------------------- Utility Functions ----------------------------

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(stored_data, f)

def generate_key(passkey: str, salt: bytes) -> bytes:
    """Generate a Fernet key using PBKDF2."""
    key = pbkdf2_hmac('sha256', passkey.encode(), salt, 100000, dklen=32)
    return base64.urlsafe_b64encode(key)

def encrypt_data(data: str, passkey: str):
    salt = os.urandom(16)
    key = generate_key(passkey, salt)
    fernet = Fernet(key)
    encrypted_text = fernet.encrypt(data.encode()).decode()
    return encrypted_text, base64.b64encode(salt).decode()

def decrypt_data(encrypted_text: str, passkey: str, salt: str):
    try:
        key = generate_key(passkey, base64.b64decode(salt.encode()))
        fernet = Fernet(key)
        decrypted_text = fernet.decrypt(encrypted_text.encode()).decode()
        return decrypted_text
    except Exception:
        return None

# --------------------------- Session State ----------------------------

if "page" not in st.session_state:
    st.session_state.page = "home"
if "username" not in st.session_state:
    st.session_state.username = None
if "login_attempts" not in st.session_state:
    st.session_state.login_attempts = 0
if "locked_until" not in st.session_state:
    st.session_state.locked_until = 0

# --------------------------- Page Navigation ----------------------------

def go_to(page):
    st.session_state.page = page

# --------------------------- Pages ----------------------------

def home_page():
    st.title("🔐 Secure Data Encryption System")

    st.write("Welcome to the secure data vault!")
    st.button("Insert Data", on_click=go_to, args=("insert",))
    st.button("Retrieve Data", on_click=go_to, args=("retrieve",))

def login_page():
    st.title("🔐 Login")

    if time.time() < st.session_state.locked_until:
        st.error(f"Too many attempts. Try again in {int(st.session_state.locked_until - time.time())} seconds.")
        return

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in LOGIN_CREDENTIALS and LOGIN_CREDENTIALS[username] == password:
            st.success("Login successful!")
            st.session_state.username = username
            st.session_state.login_attempts = 0
            go_to("home")
        else:
            st.session_state.login_attempts += 1
            st.error("Invalid credentials.")
            if st.session_state.login_attempts >= 3:
                st.session_state.locked_until = time.time() + LOCKOUT_TIME
                st.error("Too many attempts! Locked out.")

def insert_data_page():
    st.title("📝 Insert Data")

    user = st.text_input("Enter a unique user ID")
    plaintext = st.text_area("Enter text to encrypt")
    passkey = st.text_input("Enter passkey", type="password")

    if st.button("Store Securely"):
        if user and plaintext and passkey:
            encrypted_text, salt = encrypt_data(plaintext, passkey)
            stored_data[user] = {
                "encrypted_text": encrypted_text,
                "salt": salt
            }
            save_data()
            st.success("Data stored securely!")
        else:
            st.warning("Please fill all fields.")

    st.button("Back", on_click=go_to, args=("home",))

def retrieve_data_page():
    st.title("🔍 Retrieve Data")

    user = st.text_input("Enter your user ID")
    passkey = st.text_input("Enter your passkey", type="password")

    if st.button("Decrypt"):
        if user in stored_data:
            result = decrypt_data(
                stored_data[user]["encrypted_text"],
                passkey,
                stored_data[user]["salt"]
            )
            if result:
                st.success("Decryption successful!")
                st.text_area("Decrypted Text", value=result, height=150)
                st.session_state.login_attempts = 0
            else:
                st.session_state.login_attempts += 1
                st.error("Incorrect passkey.")
                st.warning(f"Attempts left: {3 - st.session_state.login_attempts}")
                if st.session_state.login_attempts >= 3:
                    st.session_state.locked_until = time.time() + LOCKOUT_TIME
                    go_to("login")
        else:
            st.error("User ID not found.")

    st.button("Back", on_click=go_to, args=("home",))

# --------------------------- Render Pages ----------------------------

if st.session_state.page == "home":
    home_page()
elif st.session_state.page == "login":
    login_page()
elif st.session_state.page == "insert":
    insert_data_page()
elif st.session_state.page == "retrieve":
    retrieve_data_page()