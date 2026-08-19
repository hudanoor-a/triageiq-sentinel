import pandas as pd
import joblib
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report


def train(data_path, model_path):
    print(f"Loading dataset from {data_path}")
    df = pd.read_csv(data_path)

    print(f"Dataset shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")

    df = df[['Ticket Description', 'Ticket Type', 'Ticket Priority']].dropna()
    df.columns = ['text', 'category', 'priority']
    df['text'] = df['text'].str.strip().str.lower()

    print(f"Training samples: {len(df)}")
    print(f"Categories: {df['category'].unique()}")
    print(f"Priorities: {df['priority'].unique()}")

    X = df['text']
    y_category = df['category']
    y_priority = df['priority']
    X_train, X_test, yc_train, yc_test, yp_train, yp_test = train_test_split(
        X, y_category, y_priority,
        test_size=0.2, random_state=42
    )

    category_pipeline = Pipeline(
        [('tfidf', TfidfVectorizer(
            max_features=5000, ngram_range=(1, 2))),
            ('clf', LogisticRegression(max_iter=1000))]
        )
    priority_pipeline = Pipeline(
        [('tfidf', TfidfVectorizer(
            max_features=5000, ngram_range=(1, 2))),
            ('clf', LogisticRegression(max_iter=1000))]
        )
    print("Training category classifier---")
    category_pipeline.fit(X_train, yc_train)
    yc_pred = category_pipeline.predict(X_test)
    print("Category classification report:")
    print(classification_report(yc_test, yc_pred))

    print("Training priority classifier---")
    priority_pipeline.fit(X_train, yp_train)
    yp_pred = priority_pipeline.predict(X_test)
    print("Priority classification report:")
    print(classification_report(yp_test, yp_pred))

    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump({'category': category_pipeline, 'priority': priority_pipeline}, model_path)
    print(f"Model saved to {model_path}")


if __name__ == '__main__':
    train(data_path='data/raw_tickets.csv', model_path='triageiq/models/triage_model.joblib')
