import joblib
import pandas as pd

from fastapi import FastAPI
from pydantic import BaseModel, Field


# ---------------------------------------------------
# Load trained clustering model
# ---------------------------------------------------

model_data = joblib.load(
    "models/customer_segmentation_pipeline.pkl"
)

pipeline = model_data["pipeline"]
reference_date = model_data["reference_date"]


# ---------------------------------------------------
# FastAPI application
# ---------------------------------------------------

app = FastAPI(
    title="Customer Segmentation API",
    description="API for K-Means customer segmentation",
    version="1.0.0"
)


# ---------------------------------------------------
# Input schema
# ---------------------------------------------------

class CustomerData(BaseModel):

    Income: float = Field(..., ge=0 )

    Recency: int = Field(..., ge=0)

    NumDealsPurchases: int = Field(..., ge=0)

    NumWebVisitsMonth: int = Field(..., ge=0)

    Complain: int = Field(..., ge=0, le=1)

    CustomerYear: int = Field(..., ge=1900)

    CustomerMonth: int = Field(..., ge=1, le=12)

    CustomerTenureDays: int = Field(..., ge=0)

    TotalSpend: float = Field(..., ge=0)

    TotalPurchases: int = Field(..., ge=0)

    TotalChildren: int = Field(..., ge=0)

    TotalCampaignAccepted: int = Field(..., ge=0)

    Age: int = Field(..., ge=0)

    Education: str

    Living_With: str


# ---------------------------------------------------
# Response schema
# ---------------------------------------------------

class ClusterResponse(BaseModel):

    cluster: int

    customer_segment: str


# ---------------------------------------------------
# Home endpoint
# ---------------------------------------------------

@app.get("/")
def home():

    return {
        "message": "Customer Segmentation API is running"
    }


# ---------------------------------------------------
# Prediction endpoint
# ---------------------------------------------------

@app.post("/predict", response_model=ClusterResponse)
def predict_cluster(data: CustomerData):

    input_data = pd.DataFrame([{

        "Income": data.Income,

        "Recency": data.Recency,

        "NumDealsPurchases": data.NumDealsPurchases,

        "NumWebVisitsMonth": data.NumWebVisitsMonth,

        "Complain": data.Complain,

        "CustomerYear": data.CustomerYear,

        "CustomerMonth": data.CustomerMonth,

        "CustomerTenureDays": data.CustomerTenureDays,

        "TotalSpend": data.TotalSpend,

        "TotalPurchases": data.TotalPurchases,

        "TotalChildren": data.TotalChildren,

        "TotalCampaignAccepted": data.TotalCampaignAccepted,

        "Age": data.Age,

        "Education": data.Education,

        "Living_With": data.Living_With

    }])


    # Predict cluster

    cluster = pipeline.predict(input_data)[0]

    cluster = int(cluster)


    # Simple segment names

    segment_names = {
        0: "Customer Segment 0",
        1: "Customer Segment 1",
        2: "Customer Segment 2",
        3: "Customer Segment 3",
        4: "Customer Segment 4"
    }


    return ClusterResponse(
        cluster=cluster,
        customer_segment=segment_names[cluster]
    )