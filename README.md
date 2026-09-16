# 🛡️ Credit Card Fraud Detection Web App

A multi-page web application built with **Python & Streamlit** that detects fraudulent transactions using Machine Learning.

---

## 📌 Features

- 🔐 **User Registration & Login** — Secure authentication with hashed passwords
- ✅ **Form Validation** — Email format, 10-digit phone, password strength checks
- 🚫 **Login Attempt Limit** — Account locks after 3 failed login attempts
- 💳 **Fraud Detection** — ML model predicts if a transaction is fraudulent
- 🤖 **XAI Reasoning** — Explains *why* a transaction looks suspicious
- 🔥 **Risk Score Gauge** — Visual speedometer chart (Green → Yellow → Red)
- 🔄 **Auto-Fill** — Random transaction from dataset for quick testing
- ⏱️ **Timestamp** — Every transaction saved with date & time
- 📊 **Interactive Dashboard** — Charts, filters, and personal transaction history
- 📁 **Transaction History** — Every check is saved per user
- 📄 **PDF Report Download** — Download full transaction history as PDF
- 🔑 **Admin Panel** — Password protected panel to manage all users & data

---

## 🗂️ Project Structure

```
fraud_detection/
├── app.py                        # Main app — Login, Register, Navigation
├── pages/
│   ├── 1_Fraud_Detection.py      # Fraud prediction page
│   ├── 2_Dashboard.py            # Dashboard & analytics page
│   └── Admin.py                  # Admin panel (password protected)
├── fraud_model.pkl               # Trained ML model
├── cleaned_fraud_dataset.xls     # Dataset used for auto-fill
├── users.json                    # Stores registered users
└── user_history.json             # Stores transaction history per user
```

---

## 🛠️ Tech Stack

| Technology | Usage |
|---|---|
| Python | Core language |
| Streamlit | Web app framework |
| Scikit-learn / Joblib | ML model training & loading |
| Pandas & NumPy | Data handling |
| Plotly | Interactive charts & gauge |
| Hashlib | Password hashing (SHA-256) |
| FPDF2 | PDF report generation |
| JSON | Data storage |

---

## 🚀 How to Run

**Step 1 — Install dependencies**
```bash
pip install streamlit pandas numpy plotly scikit-learn joblib fpdf2
```

**Step 2 — Make sure these files are in your project folder**
```
app.py
fraud_model.pkl
cleaned_fraud_dataset.xls
users.json
user_history.json
pages/1_Fraud_Detection.py
pages/2_Dashboard.py
pages/Admin.py
```

**Step 3 — Run the app**
```bash
streamlit run app.py
```

**Step 4 — Open browser**
```
http://localhost:8501
```

---

## 📖 How to Use

1. **Register** — Create account with name, valid email, 10-digit phone & password
2. **Login** — Enter credentials and press Enter or click Login
3. **Fraud Detection** — Enter transaction details or auto-fill from dataset
4. **Check Result** — See prediction, risk score gauge, reasons & timestamp
5. **Dashboard** — View personal transaction history, charts & download PDF report
6. **Admin Panel** — Enter admin password to manage all users & data

---

## 🔒 Security Features

| Feature | Details |
|---|---|
| Password Hashing | SHA-256 encryption — passwords never stored as plain text |
| Login Attempt Limit | Locked after 3 failed attempts |
| Email Validation | Must follow valid email format (abc@gmail.com) |
| Phone Validation | Must be exactly 10 digits |
| Password Strength | Minimum 6 characters required |
| Session Management | Login state maintained across pages |
| Page Protection | All pages check login before loading |
| Admin Panel | Password protected — only owner can access |

---

## 🤖 ML Model Details

- **Input Features:**
  - Transaction Amount
  - Transaction Hour
  - Night Flag (transaction between 11PM–6AM)
  - Device Changed Flag
  - Location Mismatch Flag
  - High Amount Flag (amount > ₹10,000)

- **Output:**
  - `1` → Fraudulent Transaction 🚨
  - `0` → Safe Transaction ✅

- **Risk Score Breakdown:**
  - 🌙 Night Transaction → +20%
  - 📱 Device Changed → +20%
  - 📍 Location Mismatch → +30%
  - 💰 High Amount → +30%

---

## 🔑 Admin Panel

- View all registered users
- See transaction count per user
- View any user's transaction history
- Delete specific user history
- Delete any user account
- Clear all data at once
- Password protected access

---

## 🔄 Complete Workflow

### 1️⃣ Register / Login
```
Open App → Go to Register Page
↓
Enter Name + Email + Phone + Password
↓
Validation → SHA-256 Hash → Saved in users.json
↓
Go to Login Page → Enter Correct Details → Session Saved → Home Page ✅
```

### 2️⃣ Fraud Detection
```
Fraud Detection Page
↓
Enter Manual values OR Auto-Fill from dataset
↓
"Predict Fraud Now" → Spinner → ML Model predicts
↓
XAI Reasoning + Risk Score Gauge Chart
↓
Result — FRAUD 🚨 or SAFE ✅
↓
Saved in user_history.json with Timestamp
```

### 3️⃣ Dashboard
```
Personal History → Total, Fraud, Safe count
↓
Download PDF Report
↓
Dataset Charts — Pie, Box, Line, Top 10 Table
```

### 4️⃣ Admin Panel
```
Admin Password → Overview (Users, Transactions, Fraud, Safe)
↓
All Users Table → View / Delete any user history
↓
Delete User → Clear All Data
```

### 🗂️ Data Flow
```
Register     → users.json
Login        → session_state
Fraud Check  → user_history.json
Dashboard    → user_history.json + dataset
Admin        → users.json + user_history.json
PDF Report   → Generated from user_history.json
```

---

## 👥 Team

Built as a group project for Hackathon.

---

## 📜 License

This project is for educational purposes only.