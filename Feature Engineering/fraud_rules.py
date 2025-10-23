from flask import Flask, request, jsonify
import pandas as pd
import json
from datetime import timedelta

app = Flask(__name__)

# ==============================
# 1. Load dataset
# ==============================
CSV_PATH = r"D:\DYLAN\Intern NawaData\Feature Engineering\Fraudulent_E-Commerce_Transaction_Data.csv"
df = pd.read_csv(CSV_PATH)
df.columns = df.columns.str.lower().str.strip()

# Pastikan kolom waktu dalam format datetime
if 'transaction date' in df.columns and 'transaction hour' in df.columns:
    df['transaction_datetime'] = pd.to_datetime(df['transaction date']) + \
                                 pd.to_timedelta(df['transaction hour'], unit='h')

# ==============================
# 2. Load rules dari JSON
# ==============================
RULES_PATH = r"D:\DYLAN\Intern NawaData\Feature Engineering\fraud_rules.json"
with open(RULES_PATH, 'r') as f:
    rules_config = json.load(f)

# ==============================
# 3. Fungsi apply rules
# ==============================
def apply_fraud_rules(data):
    data = data.copy()
    for rule_name, rule_details in rules_config.items():
        col = rule_details['column']
        op = rule_details['operator']
        val = rule_details['value']

        if op == '>':
            data[rule_name] = data[col] > val
        elif op == '<':
            data[rule_name] = data[col] < val
        elif op == '==':
            data[rule_name] = data[col] == val
        elif op == '!=':
            data[rule_name] = data[col] != val
        elif op == 'between':
            data[rule_name] = data[col].between(val[0], val[1])
        else:
            data[rule_name] = False

    # Hitung total rules yang kena
    data['total_rules_triggered'] = data[list(rules_config.keys())].sum(axis=1)
    data['is_suspicious'] = data['total_rules_triggered'] > 0
    return data

# ==============================
# 4. API endpoint
# ==============================
@app.route('/detect_fraud', methods=['GET'])
def detect_fraud():
    result = apply_fraud_rules(df)
    suspicious = result[result['is_suspicious'] == True]
    return suspicious.head(10).to_json(orient='records')

# ==============================
# 5. Run API
# ==============================
if __name__ == '__main__':
    app.run(debug=True)
