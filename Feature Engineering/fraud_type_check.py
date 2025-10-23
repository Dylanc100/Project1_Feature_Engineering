# fraud_api.py
import os
import json
import pandas as pd
from flask import Flask, request, jsonify

app = Flask(__name__)

# ==========================
# 1. Tentukan lokasi file (selalu relatif ke folder script)
# ==========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, "Fraudulent_E_Commerce_Transaction_Data.csv")
rules_path = os.path.join(BASE_DIR, "fraud_type_rules.json")

print(" CSV Path:", csv_path)
print("Rules Path:", rules_path)

# ==========================
# 2. Load dataset
# ==========================
try:
    df = pd.read_csv(csv_path)
except FileNotFoundError:
    raise FileNotFoundError(f"CSV file tidak ditemukan di {csv_path}")

# ==========================
# 3. Load rules dari JSON
# ==========================
try:
    with open(rules_path, "r") as f:
        fraud_rules = json.load(f)
except FileNotFoundError:
    raise FileNotFoundError(f"JSON rules file tidak ditemukan di {rules_path}")

# ==========================
# 4. Fungsi Rule Engine
# ==========================
def check_fraud(transaction):
    detected = []
    for rule_name, rule in fraud_rules.items():
        column = rule["column"]
        condition = rule["condition"]
        value = rule["value"]

        if column not in transaction:
            continue  

        try:
            if condition == "equals" and str(transaction[column]) == str(value):
                detected.append(rule_name)
            elif condition == "greater_than" and float(transaction[column]) > float(value):
                detected.append(rule_name)
            elif condition == "less_than" and float(transaction[column]) < float(value):
                detected.append(rule_name)
        except Exception:
            continue
    return detected

# ==========================
# 5. API Routes
# ==========================
@app.route("/")
def home():
    return jsonify({"message": "Fraud Detection API is running!"})

@app.route("/check_transaction", methods=["POST"])
def check_transaction():
    transaction = request.json
    detected = check_fraud(transaction)
    return jsonify({
        "transaction": transaction,
        "fraud_types_detected": detected,
        "is_fraud": len(detected) > 0
    })

@app.route("/test_dataset", methods=["GET"])
def test_dataset():
    sample = df.sample(5).to_dict(orient="records")
    return jsonify(sample)

# ==========================
# 6. Run API
# ==========================
if __name__ == "__main__":
    app.run(debug=True)
