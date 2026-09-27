import streamlit as st
import requests


# ---------------------------------------------------
# Page configuration
# ---------------------------------------------------

st.set_page_config(
    page_title="Customer Segmentation",
    page_icon="👥",
    layout="centered"
)


# ---------------------------------------------------
# Title
# ---------------------------------------------------

st.title("Customer Segmentation")

st.write(
    "Enter customer information to identify the "
    "customer's K-Means cluster."
)


# ---------------------------------------------------
# Customer Information
# ---------------------------------------------------

st.header("Customer Information")


income = st.number_input(
    "Income",
    min_value=2000.0,
    max_value=60_0000.0,
    value=50000.0,
    step=1000.0
)


age = st.number_input(
    "Age",
    min_value=18,
    max_value=100,
    value=35,
    step=1
)


recency = st.number_input(
    "Recency",
    min_value=0,
    max_value = 100,
    value=50,
    step=1
)


# ---------------------------------------------------
# Purchase Information
# ---------------------------------------------------

st.header("Purchase Information")


num_deals_purchases = st.number_input(
    "Number of Deals Purchases",
    min_value=0,
    max_value=15,
    value=2,
    step=1
)


num_web_visits_month = st.number_input(
    "Number of Web Visits per Month",
    min_value=0,
    max_value=20,
    value=5,
    step=1
)


total_spend = st.number_input(
    "Total Spend",
    min_value=5.0,
    max_value= 3000.0,
    value=500.0,
    step=25.0
)


total_purchases = st.number_input(
    "Total Purchases",
    min_value=0,
    max_value=35,
    value = 12,
    step=1
)


# ---------------------------------------------------
# Customer Information
# ---------------------------------------------------

st.header("Customer Profile")


total_children = st.number_input(
    "Total Children",
    min_value=0,
    value=1,
    step=1
)


total_campaign_accepted = st.number_input(
    "Total Campaigns Accepted",
    min_value=0,
    max_value=6,
    value=1,
    step=1
)


complain = st.selectbox(
    "Complaint",
    [0, 1],
    format_func=lambda x: "No" if x == 0 else "Yes"
)


education = st.selectbox(
    "Education",
    [
        "Undergraduate",
        "Graduate",
        "Postgraduate"
    ]
)


living_with = st.selectbox(
    "Living With",
    [
        "Alone",
        "Partner"
    ]
)


# ---------------------------------------------------
# Customer Registration Information
# ---------------------------------------------------

st.header("📅 Customer History")


customer_year = st.number_input(
    "Customer Year",
    min_value=1900,
    max_value=2030,
    value=2014,
    step=1
)


customer_month = st.number_input(
    "Customer Month",
    min_value=1,
    max_value=12,
    value=6,
    step=1
)


customer_tenure_days = st.number_input(
    "Customer Tenure Days",
    min_value=0,
    value=500,
    step=1
)


# ---------------------------------------------------
# Prediction
# ---------------------------------------------------

st.divider()


if st.button(
    " Predict Customer Cluster",
    use_container_width=True
):

    url = "http://127.0.0.1:8000/predict"


    data = {

        "Income": income,

        "Recency": recency,

        "NumDealsPurchases": num_deals_purchases,

        "NumWebVisitsMonth": num_web_visits_month,

        "Complain": complain,

        "CustomerYear": customer_year,

        "CustomerMonth": customer_month,

        "CustomerTenureDays": customer_tenure_days,

        "TotalSpend": total_spend,

        "TotalPurchases": total_purchases,

        "TotalChildren": total_children,

        "TotalCampaignAccepted": total_campaign_accepted,

        "Age": age,

        "Education": education,

        "Living_With": living_with

    }


    try:

        response = requests.post(
            url,
            json=data
        )


        if response.status_code == 200:

            result = response.json()

            cluster = result["cluster"]

            segment = result["customer_segment"]


            st.success(
                "Customer successfully assigned to a cluster!"
            )


            st.metric(
                label="Customer Cluster",
                value=f"Cluster {cluster}"
            )


            st.info(
                f"Customer Segment: {segment}"
            )


        else:

            st.error(
                f"API Error: {response.status_code}"
            )

            st.write(response.text)


    except requests.exceptions.ConnectionError:

        st.error(
            "❌ Could not connect to FastAPI."
        )

        st.info(
            "Please start the FastAPI server first."
        )


    except Exception as e:

        st.error(
            f"Something went wrong: {str(e)}"
        )