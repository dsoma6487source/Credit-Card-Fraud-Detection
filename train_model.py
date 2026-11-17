
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    average_precision_score
)

# 1. Load dataset
data = pd.read_csv("dataset/creditcard.csv")

print("Dataset Loaded Successfully!")

# 2. Separate features and target
X = data.drop("Class", axis=1)
y = data["Class"]

# 3. Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# 4. Scale Time and Amount
scaler = StandardScaler()

X_train = X_train.copy()
X_test = X_test.copy()

X_train[["Time", "Amount"]] = scaler.fit_transform(
    X_train[["Time", "Amount"]]
)

X_test[["Time", "Amount"]] = scaler.transform(
    X_test[["Time", "Amount"]]
)

# 5. Create Random Forest model
model = RandomForestClassifier(
    n_estimators=100,
    class_weight="balanced_subsample",
    random_state=42,
    n_jobs=-1
)

# 6. Train model
print("\nTraining Model...")

model.fit(X_train, y_train)

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

# Predict test data
y_pred = model.predict(X_test)

# Calculate performance
print("\nMODEL EVALUATION")

print("Accuracy:",
      accuracy_score(y_test, y_pred))

print("Precision:",
      precision_score(y_test, y_pred, zero_division=0))

print("Recall:",
      recall_score(y_test, y_pred, zero_division=0))

print("F1 Score:",
      f1_score(y_test, y_pred, zero_division=0))

print("\nClassification Report:")
print(classification_report(y_test, y_pred, zero_division=0))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("Model Training Completed!")

# 7. Make predictions
y_pred = model.predict(X_test)

# 8. Evaluate model
print("\nClassification Report:")
print(classification_report(y_test, y_pred, zero_division=0))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print(
    "\nAverage Precision Score:",
    average_precision_score(y_test, model.predict_proba(X_test)[:, 1])
)

# 9. Save model and scaler
joblib.dump(model, "fraud_model.pkl")
joblib.dump(scaler, "scaler.pkl")

print("\nModel Saved Successfully!")
