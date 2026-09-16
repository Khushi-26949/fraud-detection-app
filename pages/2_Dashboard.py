import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import os
from fpdf import FPDF
from datetime import datetime

# --- PAGE TITLE ---
st.markdown("<h2 style='color:#4CAF50;'>📊 Advanced Fraud Detection Dashboard</h2>", unsafe_allow_html=True)
st.write("Explore fraud patterns, high-risk transactions, amount trends, hours analysis, and more.")

# --- LOGIN CHECK ---
if "user" not in st.session_state or not st.session_state.user:
    st.warning("⚠ Please login first to access Dashboard.")
    st.stop()

# --------------------------------------------------------------------
# 👤 USER PERSONAL HISTORY
# --------------------------------------------------------------------
st.markdown("### 👤 My Transaction History")

user_email = st.session_state.user["email"]
user_name  = st.session_state.user["name"]

if os.path.exists("user_history.json"):
    with open("user_history.json", "r") as f:
        history = json.load(f)

    user_data = history.get(user_email, [])

    if not user_data:
        st.info("ℹ No transactions yet — go to Fraud Detection page!")
    else:
        df_user = pd.DataFrame(user_data)

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Checks", len(df_user))
        col2.metric("🚨 Fraud", df_user[df_user["prediction"] == 1].shape[0])
        col3.metric("✅ Safe",  df_user[df_user["prediction"] == 0].shape[0])

        # ── Drop reasons column before displaying — fixes None issue ──
        display_cols = ["timestamp", "amount", "hour", "night_flag",
                        "device_flag", "loc_flag", "high_amt",
                        "prediction", "risk_score"]
        display_df = df_user[[c for c in display_cols if c in df_user.columns]]
        st.dataframe(display_df)

        # ------------------------------------------------------------
        # 📄 PDF REPORT DOWNLOAD
        # ------------------------------------------------------------
        st.markdown("### 📄 Download Your Transaction Report")

        if st.button("📥 Generate & Download PDF Report"):

            total       = len(df_user)
            fraud_count = int(df_user[df_user["prediction"] == 1].shape[0])
            safe_count  = int(df_user[df_user["prediction"] == 0].shape[0])

            pdf = FPDF()
            pdf.add_page()
            pdf.set_auto_page_break(auto=True, margin=15)

            # ── DARK NAVY HEADER BANNER ──────────────────────────────
            pdf.set_fill_color(15, 32, 65)
            pdf.rect(0, 0, 210, 40, style="F")
            pdf.set_y(8)
            pdf.set_font("Arial", "B", 20)
            pdf.set_text_color(255, 255, 255)
            pdf.cell(0, 10, "Credit Card Fraud Detection", ln=True, align="C")
            pdf.set_font("Arial", "", 11)
            pdf.set_text_color(160, 195, 255)
            pdf.cell(0, 8, "Transaction Analysis Report", ln=True, align="C")
            pdf.set_font("Arial", "I", 9)
            pdf.set_text_color(130, 165, 220)
            pdf.cell(0, 7, datetime.now().strftime("Generated on %d %B %Y at %H:%M"), ln=True, align="C")
            pdf.ln(10)

            # ── USER INFO CARD ───────────────────────────────────────
            y0 = pdf.get_y()
            pdf.set_fill_color(235, 242, 255)
            pdf.set_draw_color(80, 120, 200)
            pdf.set_line_width(0.5)
            pdf.rect(10, y0, 190, 24, style="FD")
            pdf.set_fill_color(52, 120, 220)
            pdf.rect(10, y0, 4, 24, style="F")
            pdf.set_font("Arial", "B", 11)
            pdf.set_text_color(15, 32, 65)
            pdf.set_xy(18, y0 + 4)
            pdf.cell(80, 7, f"Name  :  {user_name}")
            pdf.set_font("Arial", "", 11)
            pdf.set_xy(18, y0 + 13)
            pdf.cell(0, 7, f"Email :  {user_email}")
            pdf.set_y(y0 + 30)

            # ── SUMMARY STAT CARDS — all 3 on same line ──────────────
            pdf.set_font("Arial", "B", 13)
            pdf.set_text_color(15, 32, 65)
            pdf.cell(0, 9, "Summary", ln=True)
            pdf.ln(2)

            cards = [
                ("Total Transactions", str(total),       (52,  152, 219), (41,  128, 185)),
                ("Fraud Detected",     str(fraud_count), (231, 76,  60),  (192, 57,  43)),
                ("Safe Transactions",  str(safe_count),  (46,  204, 113), (39,  174, 96)),
            ]

            card_w  = 58
            gap     = 7
            card_y  = pdf.get_y()
            start_x = 12

            for label, value, light, dark in cards:
                pdf.set_fill_color(*light)
                pdf.rect(start_x, card_y, card_w, 24, style="F")
                pdf.set_fill_color(*dark)
                pdf.rect(start_x, card_y, card_w, 5, style="F")
                pdf.set_font("Arial", "B", 20)
                pdf.set_text_color(255, 255, 255)
                pdf.set_xy(start_x, card_y + 5)
                pdf.cell(card_w, 11, value, align="C")
                pdf.set_font("Arial", "", 9)
                pdf.set_text_color(240, 240, 240)
                pdf.set_xy(start_x, card_y + 16)
                pdf.cell(card_w, 7, label, align="C")
                start_x += card_w + gap

            pdf.set_y(card_y + 30)

            # ── TRANSACTION DETAILS TABLE ────────────────────────────
            pdf.set_font("Arial", "B", 13)
            pdf.set_text_color(15, 32, 65)
            pdf.cell(0, 9, "Transaction Details", ln=True)
            pdf.ln(2)

            pdf.set_fill_color(15, 32, 65)
            pdf.set_text_color(255, 255, 255)
            pdf.set_font("Arial", "B", 9)
            col_w   = [46, 30, 16, 28, 28, 32]
            headers = ["Timestamp", "Amount (Rs)", "Hour", "Risk Score", "Result", "Flags"]
            for i, h in enumerate(headers):
                pdf.cell(col_w[i], 9, h, border=0, fill=True, align="C")
            pdf.ln()

            for idx, row in df_user.iterrows():
                is_fraud = row.get("prediction") == 1

                if idx % 2 == 0:
                    pdf.set_fill_color(245, 249, 255)
                else:
                    pdf.set_fill_color(255, 255, 255)

                flags = []
                if int(row.get("night_flag")  or 0) == 1: flags.append("Night")
                if int(row.get("device_flag") or 0) == 1: flags.append("Dev")
                if int(row.get("loc_flag")    or 0) == 1: flags.append("Loc")
                if int(row.get("high_amt")    or 0) == 1: flags.append("Hi$")
                flags_str = " ".join(flags) if flags else "-"

                ts     = str(row.get("timestamp") or "")[:19]
                amt_v  = row.get("amount")
                amt    = f"Rs {round(float(amt_v), 2)}" if amt_v is not None else "-"
                hr     = str(int(row.get("hour") or 0))
                risk   = str(int(row.get("risk_score") or 0)) + "%"
                result = "FRAUD" if is_fraud else "SAFE"

                row_vals = [ts, amt, hr, risk, result, flags_str]

                for i, val in enumerate(row_vals):
                    if i == 4:
                        if is_fraud:
                            pdf.set_text_color(192, 57, 43)
                        else:
                            pdf.set_text_color(39, 174, 96)
                        pdf.set_font("Arial", "B", 9)
                    else:
                        pdf.set_text_color(40, 40, 40)
                        pdf.set_font("Arial", "", 9)
                    pdf.cell(col_w[i], 8, val, border=0, fill=True, align="C")
                pdf.ln()
                pdf.set_draw_color(200, 215, 235)
                pdf.line(12, pdf.get_y(), 198, pdf.get_y())

            pdf.ln(8)

            # ── FOOTER ───────────────────────────────────────────────
            pdf.set_fill_color(15, 32, 65)
            pdf.rect(0, 280, 210, 17, style="F")
            pdf.set_y(284)
            pdf.set_font("Arial", "I", 9)
            pdf.set_text_color(160, 195, 255)
            pdf.cell(0, 6, "Credit Card Fraud Detection System  |  For educational purposes only", align="C")

            pdf_path = "transaction_report.pdf"
            pdf.output(pdf_path)
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="📄 Click to Download PDF",
                    data=f,
                    file_name=f"fraud_report_{user_name}.pdf",
                    mime="application/pdf"
                )
            st.success("✅ PDF Report ready!")

else:
    st.info("ℹ No transaction history found.")

st.markdown("---")

# --------------------------------------------------------------------
# 📂 LOAD DATASET (FIXED: uses the same shared dataset, relative path,
# and read_csv — the file's content is actually CSV despite the .xls name)
# --------------------------------------------------------------------
@st.cache_data
def load_data():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_PATH = os.path.join(BASE_DIR, "pages", "cleaned_fraud_dataset.xls")
    return pd.read_csv(DATA_PATH)

df = load_data()
st.success("✅ Dataset Loaded Successfully!")

# --------------------------------------------------------------------
# 🔍 FILTER BAR
# --------------------------------------------------------------------
st.markdown("### 🔎 Filters")
colf1, colf2, colf3 = st.columns(3)
fraud_filter  = colf1.selectbox("Filter by Class", ["All", "Normal", "Fraud"])
hour_filter   = colf2.slider("Filter by Hour Range", 0, 23, (0, 23))
amount_filter = colf3.slider("Amount Range", 0, int(df["Amount"].max()), (0, int(df["Amount"].max())))

filtered_df = df.copy()
if fraud_filter != "All":
    filtered_df = filtered_df[filtered_df["Class"] == (1 if fraud_filter == "Fraud" else 0)]
filtered_df = filtered_df[
    (filtered_df["Hour"]   >= hour_filter[0])   & (filtered_df["Hour"]   <= hour_filter[1]) &
    (filtered_df["Amount"] >= amount_filter[0]) & (filtered_df["Amount"] <= amount_filter[1])
]

# --------------------------------------------------------------------
# 📌 METRICS CARDS
# --------------------------------------------------------------------
st.markdown("### 📌 Key Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Transactions", len(filtered_df))
col2.metric("Normal", filtered_df[filtered_df["Class"] == 0].shape[0])
col3.metric("Fraud",  filtered_df[filtered_df["Class"] == 1].shape[0])
fraud_percent = round((filtered_df[filtered_df["Class"] == 1].shape[0] / len(filtered_df)) * 100, 2) if len(filtered_df) > 0 else 0
col4.metric("Fraud %", f"{fraud_percent}%")
st.markdown("---")

# --------------------------------------------------------------------
# 1️⃣ PIE CHART
# --------------------------------------------------------------------
st.markdown("### 🔍 Fraud vs Normal Distribution")
class_counts = filtered_df["Class"].value_counts().reset_index()
class_counts.columns = ["Class", "Count"]
fig1 = px.pie(class_counts, names="Class", values="Count",
              title="Fraud vs Normal Distribution", color="Class", hole=0.4)
st.plotly_chart(fig1, use_container_width=True)

# --------------------------------------------------------------------
# 2️⃣ BOX CHART
# --------------------------------------------------------------------
st.markdown("### 💰 Amount Distribution (Normal vs Fraud)")
fig2 = px.box(filtered_df, x="Class", y="Amount", color="Class",
              title="Amount Comparison: Normal vs Fraud")
st.plotly_chart(fig2, use_container_width=True)

# --------------------------------------------------------------------
# 3️⃣ HOURLY LINE CHART
# --------------------------------------------------------------------
if "Hour" in df.columns:
    st.markdown("### ⏰ Transactions by Hour (Normal vs Fraud)")
    hourly = filtered_df.groupby("Hour")["Class"].value_counts().unstack(fill_value=0)
    fig3 = px.line(hourly, x=hourly.index, y=[0, 1],
                   labels={"value": "Count", "Hour": "Hour of Day"},
                   title="Hourly Transaction Trend")
    st.plotly_chart(fig3, use_container_width=True)
else:
    st.warning("⚠ 'Hour' column not found in dataset.")

st.markdown("---")

# --------------------------------------------------------------------
# 4️⃣ HIGH RISK TABLE
# --------------------------------------------------------------------
st.markdown("### 🚨 Top 10 High Amount & High Risk Transactions")
high_risk_df = filtered_df.sort_values(by="Amount", ascending=False).head(10)
st.dataframe(high_risk_df)

# --------------------------------------------------------------------
# 5️⃣ DATASET PREVIEW
# --------------------------------------------------------------------
with st.expander("📄 Full Dataset Preview (Filtered)"):
    st.dataframe(filtered_df)

st.markdown("<hr><center>Made with ❤️ | Advanced ML Dashboard</center>", unsafe_allow_html=True)