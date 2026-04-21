from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from imblearn.over_sampling import SMOTE
import joblib
import os

def train_model(X_train, y_train, use_smote=True):
    
    if use_smote:
        smote = SMOTE(random_state=42)
        X_train, y_train = smote.fit_resample(X_train, y_train)

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    return model

def evaluate_model(model, X_test, y_test):
    preds = model.predict(X_test)
    report = classification_report(y_test, preds)
    print(report)

def save_model(model, path="models/model.pkl"):
    os.makedirs("models", exist_ok=True)
    joblib.dump(model, path)