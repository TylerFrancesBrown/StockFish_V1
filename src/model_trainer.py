from data_loader import get_historical_data
from feature_engineering import create_features, create_labels
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report

def train_and_evaluate(symbol, start, end):
    # 1) Load data
    df = get_historical_data(symbol, start, end)

    # 2) Feature & label
    feat_df = create_features(df)
    y, X = create_labels(feat_df)

    # 3) Time-based split (80% train / 20% test)
    split = int(len(X)*0.8)
    X_train, X_test = X.iloc[:split], X.iloc[split:]
    y_train, y_test = y.iloc[:split], y.iloc[split:]

    # 4) Train
    model = XGBClassifier(use_label_encoder=False, eval_metric='logloss')
    drop_cols = ['o','h','l','c','v','n','vw','return']
    model.fit(X_train.drop(columns=drop_cols), y_train)

    # 5) Evaluate
    preds  = model.predict(X_test.drop(columns=drop_cols))
    probas = model.predict_proba(X_test.drop(columns=drop_cols))[:,1]

    print("Accuracy:", accuracy_score(y_test, preds))
    print("ROC AUC: ", roc_auc_score(y_test, probas))
    print(classification_report(y_test, preds))
    return model

if __name__ == "__main__":
    train_and_evaluate(
      "AAPL",
      "2024-04-01T09:30:00-04:00",
      "2024-04-01T16:00:00-04:00"
    )
