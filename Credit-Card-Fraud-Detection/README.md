# 📘 **Credit Card Fraud Detection Using Imbalanced Datasets**

This project focuses on identifying fraudulent credit-card transactions when working with **highly imbalanced datasets**. The notebook explores multiple resampling techniques, evaluates model performance, and demonstrates correct vs. incorrect cross-validation approaches to avoid data leakage.

---

# ⭐ **Project Overview**

Financial fraud detection is a classic case of imbalanced data — fraudulent transactions are less than **0.2%** of total data. A standard model trained on raw data tends to predict **all transactions as non-fraud**, achieving misleadingly high accuracy.
This project demonstrates how to correct this using:

* Random undersampling
* Random oversampling
* SMOTE (Synthetic Minority Oversampling Technique)
* Proper cross-validation to avoid overfitting
* Logistic Regression modelling
* Metrics: Accuracy, Precision, Recall, F1-score, Confusion Matrix

---

# 🏗️ **Project Architecture (Production Upgrade)**

This project has been extended from a notebook-based experiment into a **production-ready ML pipeline**:

```id="arch1"
Data → Preprocessing → SMOTE → Model Training → Evaluation → Model Saving → API Inference
```

### Components:

* 📊 **Notebook** → EDA, experimentation, learning
* ⚙️ **Training Pipeline (`run_training.py`)** → automated model training
* 🤖 **Model Artifact (`models/model.pkl`)** → saved trained model
* 🚀 **FastAPI (`app/main.py`)** → real-time fraud prediction API
* 🐳 **Docker Support** → containerized deployment

---

# 📊 **Key Results & Insights**

| Metric            | Value                       |
| ----------------- | --------------------------- |
| Accuracy          | ~99%                        |
| Recall (Fraud)    | ~90%                        |
| Precision (Fraud) | ~10–12%                     |
| PR-AUC            | Improved from ~0.01 → ~0.75 |

### 🧠 Key Insight:

> Accuracy is misleading for imbalanced datasets — **Recall and PR-AUC are the true indicators of performance in fraud detection systems**

---

# ⚙️ **How to Run the Project**

## 1️⃣ Clone Repository

```bash id="clone1"
git clone https://github.com/<your-username>/Credit-Card-Fraud-Detection.git
cd Credit-Card-Fraud-Detection
```

---

## 2️⃣ Setup Environment

```bash id="env1"
python -m venv venv
source venv/bin/activate   # (Linux/Mac)
venv\Scripts\activate      # (Windows)
pip install -r requirements.txt
```

---

## 3️⃣ Train Model

```bash id="train1"
python run_training.py
```

👉 This will:

* Train model using SMOTE
* Evaluate performance
* Save model to `models/model.pkl`

---

## 4️⃣ Run API

```bash id="api1"
python -m uvicorn app.main:app --reload
```

---

## 5️⃣ Test API

```bash id="api2"
POST /predict
```

Example input:

```json id="json1"
{
  "V1": 0.1,
  "V2": -1.2,
  "V3": 0.5,
  ...
}
```

---

# 🧩 **Code Walkthrough**

## **1. Importing Libraries**

Key libraries used:

* `numpy`, `pandas` → data manipulation
* `matplotlib`, `seaborn` → visualization
* `sklearn` → ML model, resampling, metrics
* `imblearn` → SMOTE & oversampling

Purpose: Prepares the scientific stack required for analysis, modelling, and evaluation.

---

## **2. Dataset Loading & Basic Exploration**

* Loads the dataset (`creditcard.csv`).
* Inspects:

  * Shape
  * Null values
  * Display of fraud vs. non-fraud counts
* Observes extreme class imbalance (~99.83% non-fraud).

Purpose: Understand data scale, imbalance severity, and distribution.

---

## **3. Feature Correlation & EDA**

* Plots correlation matrix.
* Checks distributions of:

  * legitimate transactions
  * fraudulent transactions

Purpose: Helps reveal patterns and understand whether fraud has distinguishable feature behavior.

---

## **4. Train/Test Splitting**

* Uses `train_test_split()` with `stratify=y`.
* Ensures both training & test sets preserve original imbalance.

Purpose: Prevents biased evaluation caused by uneven distribution.

---

## **5. Baseline Logistic Regression on Imbalanced Data**

* Trains a simple classifier without resampling.
* Evaluates:

  * Accuracy
  * Recall (very low)
  * Confusion matrix (model predicts almost all non-fraud)

Purpose: Shows why imbalanced datasets break standard ML models.

---

## **6. Undersampling (Reducing Non-Fraud Cases)**

* Randomly downsamples the majority class.
* Trains Logistic Regression on balanced subset.
* Performs cross-validation on the reduced dataset.

Observations:

* Improved recall on fraud class
* Reduced accuracy due to information loss

Purpose: Faster training, improved fraud detection, but with trade-offs.

---

## **7. Oversampling the Minority Class**

* Random oversampling duplicates fraud cases.
* Model trained on oversampled dataset.
* Evaluation performed on original test set.

Purpose: Avoids losing legitimate transaction data.

---

## **8. SMOTE (Synthetic Minority Oversampling Technique)**

* Generates synthetic fraud samples rather than duplicating.
* Applied **inside** cross-validation loop (correct approach).

Purpose: Better generalization with more realistic synthetic samples.

---

## **9. Demonstration of Overfitting (Incorrect CV)**

The notebook highlights a **common mistake**:

❌ Applying SMOTE **before** cross-validation  
✔️ Correct: Apply SMOTE **during** each CV fold

Purpose: Shows how incorrect application leads to unrealistic metrics and data leakage.

---

## **10. Confusion Matrix Comparisons**

Plots confusion matrices for:

* SMOTE model
* Original model
* Undersample model
* Oversample model

Purpose: Visual comparison of fraud detection performance across techniques.

---

## **11. Final Conclusion**

* SMOTE shows balanced precision-recall and good fraud detection.
* Future improvements: XGBoost, LightGBM, Isolation Forest, NN models, feature engineering.