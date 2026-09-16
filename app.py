import streamlit as st
import json
import os
import re
import hashlib

st.set_page_config(page_title="Fraud Detection App", layout="wide")

# ---------- VALIDATION FUNCTIONS ----------
def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def is_valid_phone(phone):
    return phone.isdigit() and len(phone) == 10

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ---------- SESSION INITIALIZATION ----------
if "user" not in st.session_state:
    st.session_state.user = None

if "login_attempts" not in st.session_state:
    st.session_state.login_attempts = 0

# ---------- LOAD / CREATE USER DATABASE ----------
def load_users():
    if not os.path.exists("users.json"):
        return {}
    with open("users.json", "r") as f:
        return json.load(f)

def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f, indent=4)

users_db = load_users()

# ---------- SIDEBAR ----------
st.sidebar.title("Navigation")

# Logout Button
if st.session_state.user:
    if st.sidebar.button("🚪 Logout"):
        st.session_state.user = None
        st.session_state.login_attempts = 0
        st.sidebar.success("Logged out successfully!")
        st.rerun()
else:
    st.sidebar.info("Please Login First.")

page = st.sidebar.selectbox(
    "Go to Page",
    ["Login", "Register", "Home", "Fraud Detection", "Dashboard","Admin"]
)

# ---------- LOGIN PAGE ----------
if page == "Login":
    st.markdown("## 🔐 Login")

    with st.form("login_form"):
        email = st.text_input("Email")
        name = st.text_input("Full Name")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            if st.session_state.login_attempts >= 3:
                st.error("🚫 Too many failed attempts! Please restart the app.")
                st.stop()
            elif email in users_db and \
               users_db[email]["name"] == name and \
               users_db[email].get("password") == hash_password(password):
                st.session_state.user = users_db[email]
                st.session_state.login_attempts = 0
                st.success("✅ Login Successful!")
                st.rerun()
            else:
                st.session_state.login_attempts += 1
                remaining = 3 - st.session_state.login_attempts
                if remaining > 0:
                    st.error(f"❌ Incorrect details! {remaining} attempts remaining.")
                else:
                    st.error("🚫 Too many failed attempts! Please restart the app.")

# ---------- REGISTER PAGE ----------
elif page == "Register":
    st.markdown("## 📝 Create New Account")

    with st.form("register_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        phone = st.text_input("Phone Number")
        password = st.text_input("Password", type="password")
        confirm = st.text_input("Confirm Password", type="password")
        submitted = st.form_submit_button("Register")

        if submitted:
            if not name or not email or not phone or not password:
                st.error("❌ All fields are required.")
            elif not is_valid_email(email):
                st.error("❌ Please enter a valid email — e.g: abc@gmail.com")
            elif not is_valid_phone(phone):
                st.error("❌ Phone number must be exactly 10 digits.")
            elif password != confirm:
                st.error("❌ Passwords do not match!")
            elif len(password) < 6:
                st.error("❌ Password must be at least 6 characters.")
            elif email in users_db:
                st.error("❌ This email is already registered!")
            elif any(user["phone"] == phone for user in users_db.values()):
                st.error("❌ This phone number is already in use!")
            else:
                users_db[email] = {
                    "name": name,
                    "email": email,
                    "phone": phone,
                    "password": hash_password(password)
                }
                save_users(users_db)
                st.success("✅ Account created! Please login now.")
                st.rerun()

# ---------- HOME PAGE ----------
elif page == "Home":
    if not st.session_state.user:
        st.warning("Please login first.")
        st.stop()

    st.markdown(f"## 👋 Welcome, {st.session_state.user['name']}")
    st.write("This app allows fraud prediction and transaction analysis.")

# ---------- FRAUD DETECTION ----------
elif page == "Fraud Detection":
    if not st.session_state.user:
        st.warning("⚠ Please login to access Fraud Detection.")
        st.stop()

    st.switch_page("pages/1_Fraud_Detection.py")

# ---------- DASHBOARD ----------
elif page == "Dashboard":
    if not st.session_state.user:
        st.warning("⚠ Please login to access the Dashboard.")
        st.stop()

    st.switch_page("pages/2_Dashboard.py")
    # ---------- ADMIN PAGE ----------
elif page == "Admin":
    st.markdown("## 🔑 Admin Login")

    admin_pass = st.text_input("Enter Admin Password", type="password")

    if st.button("Access Admin Panel"):
        if admin_pass == "2023":  # ← apna password yahan rakho
            st.session_state.admin = True
            st.rerun()
        else:
            st.error("❌ Wrong Admin Password!")

    if st.session_state.get("admin"):
        st.switch_page("pages/Admin.py")