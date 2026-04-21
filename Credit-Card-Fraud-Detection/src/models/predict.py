import joblib
import pandas as pd

def load_model(path="models/model.pkl"):
    return joblib.load(path)

def predict(data: dict):
    model = load_model()

    df = pd.DataFrame([data])
    prediction = model.predict(df)

    return int(prediction[0])