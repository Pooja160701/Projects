import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "netflix_titles.csv")

def encode_rating(r):
    if pd.isna(r): return 0
    mapping = {
        "TV-Y": 1, "TV-Y7": 1, "TV-G": 1,
        "TV-PG": 2, "PG": 2,
        "TV-14": 3, "PG-13": 3,
        "R": 4, "TV-MA": 4,
        "NC-17": 5
    }
    return mapping.get(r, 0)

def parse_duration(d):
    if pd.isna(d): return 0
    try:
        num = int(str(d).split()[0])
    except:
        return 0

    if "min" in str(d):
        return num
    if "Season" in str(d):
        return num * 60
    return num

def main():
    print("Loading data from:", DATA_FILE)
    df = pd.read_csv(DATA_FILE)

    # Remove missing core columns
    df = df.dropna(subset=["type", "release_year", "duration", "description"])

    # Feature engineering
    df["rating_enc"] = df["rating"].apply(encode_rating)
    df["duration_num"] = df["duration"].apply(parse_duration)
    df["title_length"] = df["title"].fillna("").apply(lambda x: len(x))
    df["description_length"] = df["description"].apply(lambda x: len(str(x)))

    df["has_season_word"] = df["duration"].apply(lambda x: 1 if "Season" in str(x) else 0)
    df["is_kids"] = df["rating"].apply(lambda r: 1 if r in ["TV-Y", "TV-Y7", "TV-G"] else 0)

    # Country-based flags
    df["country"] = df["country"].fillna("")
    df["is_US"] = df["country"].apply(lambda c: 1 if "United States" in c else 0)
    df["is_India"] = df["country"].apply(lambda c: 1 if "India" in c else 0)

    # Feature matrix
    feature_cols = [
        "release_year",
        "rating_enc",
        "duration_num",
        "title_length",
        "description_length",
        "has_season_word",
        "is_kids",
        "is_US",
        "is_India"
    ]

    X = df[feature_cols]
    y = df["type"].apply(lambda t: 1 if t == "TV Show" else 0)

    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Train model
    model = LogisticRegression(max_iter=2000)
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print("Improved Accuracy:", acc)
    print("Classification Report:\n", classification_report(y_test, y_pred))

    # Save model + features
    out_dir = os.path.dirname(__file__)
    joblib.dump(model, os.path.join(out_dir, "model.joblib"))
    joblib.dump(feature_cols, os.path.join(out_dir, "feature_columns.joblib"))

    print("Saved improved model and feature_columns to:", out_dir)

if __name__ == "__main__":
    main()