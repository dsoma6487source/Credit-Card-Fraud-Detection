from database import init_db, save_transaction, get_transactions, get_stats
from database import init_db, save_transaction, get_transactions
from flask import Flask, request, jsonify
import pandas as pd
import joblib

app = Flask(__name__)

init_db()

# Load trained ML model
model = joblib.load("fraud_model.pkl")
scaler = joblib.load("scaler.pkl")

# Features used during training
FEATURES = (
    ["Time"] +
    [f"V{i}" for i in range(1, 29)] +
    ["Amount"]
)


from flask import render_template

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/health")
def health():
    return jsonify({
        "status": "success",
        "message": "Fraud Detection Backend is Working!"
    })


@app.route("/predict", methods=["POST"])
def predict():

    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "JSON data is required"}), 400

        # Check required features
        missing = [f for f in FEATURES if f not in data]

        if missing:
            return jsonify({
                "error": "Missing transaction features",
                "missing_features": missing
            }), 400

        # Prepare transaction
        transaction = pd.DataFrame(
            [[float(data[f]) for f in FEATURES]],
            columns=FEATURES
        )

        # Scale Time and Amount
        transaction[["Time", "Amount"]] = scaler.transform(
            transaction[["Time", "Amount"]]
        )

        # Predict
        prediction = model.predict(transaction)[0]

        probability = model.predict_proba(transaction)[0][1]

        result = (
            "Fraudulent Transaction"
            if prediction == 1
            else "Legitimate Transaction"
        )
        save_transaction(
            float(data["Amount"]),
            int(prediction),
            result,
            float(probability)
            )

        return jsonify({
            "prediction": int(prediction),
            "result": result,
            "fraud_probability": round(float(probability), 4)
        })

    except (ValueError, TypeError):
        return jsonify({
            "error": "Transaction features must be numeric"
        }), 400

    except Exception:
        return jsonify({
            "error": "Unable to process transaction"
        }), 500

@app.route("/history")
def history():

    transactions = get_transactions()

    return jsonify(transactions)

@app.route("/stats")
def stats():

    return jsonify(get_stats())


if __name__ == "__main__":
    app.run(debug=False)