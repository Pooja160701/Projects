from src.data.load_data import load_data
from src.features.preprocess import split_data
from src.models.train import train_model, evaluate_model, save_model

def run():
    df = load_data("data/creditcard.csv")

    X_train, X_test, y_train, y_test = split_data(df)

    model = train_model(X_train, y_train, use_smote=True)

    evaluate_model(model, X_test, y_test)

    save_model(model)

if __name__ == "__main__":
    run()