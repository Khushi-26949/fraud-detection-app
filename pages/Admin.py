import streamlit as st
import json
import os
import pandas as pd
from fpdf import FPDF
from datetime import datetime

# --- ADMIN CHECK ---
if not st.session_state.get("admin"):
    st.warning("⚠ Access Denied! Please login as Admin.")
    st.stop()

# --- PAGE TITLE ---
st.markdown("<h2 style='color:#FF4B4B;'>🔐 Admin Panel</h2>", unsafe_allow_html=True)
st.write("Manage all users and their transaction history.")

# --- LOAD DATA ---
def load_users():
    if not os.path.exists("users.json"):
        return {}
    with open("users.json", "r") as f:
        return json.load(f)

def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f, indent=4)

def load_history():
    if not os.path.exists("user_history.json"):
        return {}
    with open("user_history.json", "r") as f:
        return json.load(f)

def save_history(history):
    with open("user_history.json", "w") as f:
        json.dump(history, f, indent=4)

users_db = load_users()
history_db = load_history()

# --------------------------------------------------------------------
# 📌 OVERVIEW METRICS
# --------------------------------------------------------------------
st.markdown("### 📌 Overview")

total_users = len(users_db)
total_transactions = sum(len(v) for v in history_db.values())
total_fraud = sum(
    sum(1 for r in records if r["prediction"] == 1)
    for records in history_db.values()
)
total_safe = total_transactions - total_fraud

col1, col2, col3, col4 = st.columns(4)
col1.metric("👥 Total Users", total_users)
col2.metric("💳 Total Transactions", total_transactions)
col3.metric("🚨 Total Fraud", total_fraud)
col4.metric("✅ Total Safe", total_safe)

st.markdown("---")

# --------------------------------------------------------------------
# 👥 ALL USERS TABLE
# --------------------------------------------------------------------
st.markdown("### 👥 All Registered Users")

if not users_db:
    st.info("No users registered yet.")
else:
    user_rows = []
    for email, user in users_db.items():
        user_history = history_db.get(email, [])
        fraud_count = sum(1 for r in user_history if r["prediction"] == 1)
        safe_count = len(user_history) - fraud_count
        user_rows.append({
            "Name": user["name"],
            "Email": email,
            "Phone": user.get("phone", "N/A"),
            "Total Transactions": len(user_history),
            "🚨 Fraud": fraud_count,
            "✅ Safe": safe_count
        })

    df_users = pd.DataFrame(user_rows)
    st.dataframe(df_users, use_container_width=True)

st.markdown("---")

# --------------------------------------------------------------------
# 🔍 VIEW USER HISTORY
# --------------------------------------------------------------------
st.markdown("### 🔍 View User Transaction History")

selected_email = st.selectbox("Select User", list(users_db.keys()))

if selected_email:
    user_data = history_db.get(selected_email, [])

    if not user_data:
        st.info("This user has no transactions yet.")
    else:
        df_history = pd.DataFrame(user_data)
        st.dataframe(df_history, use_container_width=True)

        # Delete user history
        if st.button(f"🗑️ Clear History for {selected_email}"):
            history_db[selected_email] = []
            save_history(history_db)
            st.success(f"✅ History cleared for {selected_email}!")
            st.rerun()

st.markdown("---")

# --------------------------------------------------------------------
# 🗑️ DELETE USER
# --------------------------------------------------------------------
st.markdown("### 🗑️ Delete a User")

delete_email = st.selectbox("Select User to Delete", list(users_db.keys()), key="delete")

if st.button(f"❌ Delete User: {delete_email}"):
    del users_db[delete_email]
    save_users(users_db)
    if delete_email in history_db:
        del history_db[delete_email]
        save_history(history_db)
    st.success(f"✅ User {delete_email} deleted!")
    st.rerun()

st.markdown("---")

# --------------------------------------------------------------------
# 🗑️ CLEAR ALL DATA
# --------------------------------------------------------------------
st.markdown("### ⚠️ Danger Zone")

if st.button("🗑️ Clear ALL Users & History"):
    save_users({})
    save_history({})
    st.session_state.admin = False
    st.success("✅ All data cleared!")
    st.rerun()

# --- Logout Admin ---
st.markdown("---")
if st.button("🚪 Logout Admin"):
    st.session_state.admin = False
    st.success("Logged out from Admin Panel!")
    st.rerun()

# Footer
st.markdown("<hr><center>🔐 Admin Panel | Fraud Detection App</center>", unsafe_allow_html=True)