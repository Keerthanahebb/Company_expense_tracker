import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API = "http://127.0.0.1:8000"

st.title("Enterprise Expense Intelligence Dashboard")

st.sidebar.title("Controls")

option = st.sidebar.selectbox(
    "Choose Action",
    [
        "Train Model",
        "Process Expenses",
        "Drift Detection",
        "Detect Anomalies",
        "Forecast Department Expenses"
    ]
)

# TRAIN MODEL
if option == "Train Model":

    st.header("Train Expense Classification Model")

    if st.button("Train Model"):

        res = requests.post(API + "/train-model")
        data = res.json()

        st.success("Model trained successfully")
        st.json(data)


# PROCESS EXPENSES
elif option == "Process Expenses":

    st.header("Auto Categorize Expenses")

    if st.button("Process Unlabeled Expenses"):

        res = requests.post(API + "/process-expenses")
        data = res.json()

        st.success("Expenses processed")
        st.json(data)


# DRIFT DETECTION
elif option == "Drift Detection":

    st.header("Model Drift Monitoring")

    if st.button("Check Drift"):

        res = requests.get(API + "/drift-status")
        data = res.json()

        st.subheader("Drift Score")
        st.write(data)


# ANOMALY DETECTION
elif option == "Detect Anomalies":

    st.header("Department Expense Anomalies")

    if st.button("Detect Anomalies"):

        res = requests.get(API + "/department-anomalies")
        data = res.json()

        anomalies = data["anomalies"]

        if len(anomalies) == 0:
            st.success("No anomalies detected")
        else:
            df = pd.DataFrame(anomalies)

            st.subheader("Anomaly Table")
            st.dataframe(df)

            fig = px.scatter(
                df,
                x="department_id",
                y="amount",
                color="amount",
                title="Anomalous Expenses"
            )

            st.plotly_chart(fig)


# FORECASTING
elif option == "Forecast Department Expenses":

    st.header("Department Expense Forecast")

    dept = st.number_input("Department ID", min_value=1)

    if st.button("Generate Forecast"):

        res = requests.get(f"{API}/forecast/{dept}")
        data = res.json()

        if "error" in data:
            st.error(data["error"])
        else:

            df = pd.DataFrame(
                list(data["forecast"].items()),
                columns=["Month", "Predicted Spend"]
            )

            fig = px.line(
                df,
                x="Month",
                y="Predicted Spend",
                title="Forecasted Department Expenses"
            )

            st.plotly_chart(fig)

            st.dataframe(df)







# import streamlit as st
# import requests

# st.title("Company Expense Intelligence System")

# description = st.text_input("Enter expense description")

# if st.button("Predict Category"):

#     response = requests.post(
#         "http://localhost:8000/predict-category",
#         json={"description": description}
#     )

#     result = response.json()

#     st.success(f"Category: {result['category']}")
#     st.write(f"Confidence: {result['confidence']}")