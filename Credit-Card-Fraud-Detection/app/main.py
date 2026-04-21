from fastapi import FastAPI
from src.models.predict import predict

app = FastAPI(title="Fraud Detection API")

@app.get("/")
def home():
    return {"message": "Fraud Detection API Running"}

@app.post("/predict")
def predict_fraud(data: dict):
    result = predict(data)
    return {"fraud_prediction": result}