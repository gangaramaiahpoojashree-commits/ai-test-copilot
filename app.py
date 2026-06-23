
import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- CONFIG ---
st.set_page_config(page_title="AI Test Copilot", layout="wide")

# --- STORAGE FILE ---
FILE = "test_results.csv"

# Create file if not exists
if not os.path.exists(FILE):
    df_init = pd.DataFrame(columns=["Test Case ID", "Scenario", "Status", "Execution Date"])
    df_init.to_csv(FILE, index=False)

# Load data
df = pd.read_csv(FILE)

# --- SIDEBAR ---
st.sidebar.title("AI Test Copilot")
menu = st.sidebar.radio("Select Option", [
    "Generate Test Cases",
    "Update Test Results",
    "Dashboard"
])

# --- MOCK AI FUNCTION ---
def generate_test_cases(user_input):
    return [
        {"id": "TC001", "steps": "Enter data, click submit", "expected": "Validation message"},
        {"id": "TC002", "steps": "Leave fields empty", "expected": "Error shown"},
        {"id": "TC003", "steps": "Enter valid data", "expected": "Success message"}
    ]

# --- PAGE 1: AI GENERATION ---
if menu == "Generate Test Cases":
    st.title("🤖 AI Test Case Generator")

    user_input = st.text_area("Enter test scenario")

    if st.button("Generate"):
        results = generate_test_cases(user_input)

        st.subheader("Generated Test Cases")

        for test in results:
            st.write(f"**{test['id']}**")
            st.write(f"Steps: {test['steps']}")
            st.write(f"Expected: {test['expected']}")
            st.write("---")

# --- PAGE 2: UPDATE RESULTS ---
elif menu == "Update Test Results":
    st.title("🧪 Update Test Results")

    test_id = st.text_input("Test Case ID")
    scenario = st.text_input("Scenario")

    status = st.selectbox("Status", ["Pass", "Fail", "Blocked"])

    if st.button("Save Result"):
        new_entry = pd.DataFrame([{
            "Test Case ID": test_id,
            "Scenario": scenario,
            "Status": status,
            "Execution Date": datetime.now()
        }])

        new_entry.to_csv(FILE, mode='a', header=False, index=False)
        st.success("✅ Test result saved")

# --- PAGE 3: DASHBOARD ---
elif menu == "Dashboard":
    st.title("📊 Test Dashboard")

    if df.empty:
        st.warning("No test data available")
    else:
        total = len(df)
        passed = len(df[df["Status"] == "Pass"])
        failed = len(df[df["Status"] == "Fail"])
        blocked = len(df[df["Status"] == "Blocked"])
        pass_rate = (passed / total) * 100

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total", total)
        col2.metric("Passed", passed)
        col3.metric("Failed", failed)
        col4.metric("Pass %", f"{pass_rate:.1f}")

        # Pie Chart
        st.subheader("Status Distribution")
        st.bar_chart(df["Status"].value_counts())

        # Trend
        st.subheader("Execution Trend")
        df["Execution Date"] = pd.to_datetime(df["Execution Date"])
        trend = df.groupby(df["Execution Date"].dt.date).count()["Test Case ID"]
        st.line_chart(trend)

        # Table
        st.subheader("All Results")
        st.dataframe(df)
