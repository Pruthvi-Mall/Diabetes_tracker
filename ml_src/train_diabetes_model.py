import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import joblib
import os

print("Loading dataset...")

df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/diabetes.csv")

X = df.drop("Outcome", axis=1)
y = df["Outcome"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
joblib.dump(model, os.path.join(BASE_DIR, "artifacts", "diabetes_model.pkl"))

print("Model trained & saved successfully!")
