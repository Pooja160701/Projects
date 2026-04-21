from sklearn.model_selection import train_test_split

def split_data(df, target_col="Class"):
    X = df.drop(columns=[target_col])
    y = df[target_col]

    return train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )