import pandas as pd
import random

# === 1. Load dataset lama ===
# ganti path ini ke dataset aslimu
df = pd.read_csv("Fraudulent_E_Commerce_Transaction_Data.csv")

# === 2. Daftar brand & model ===
device_options = {
    "Samsung": ["Galaxy A14", "Galaxy S23", "Galaxy Note 20", "Galaxy Z Flip5"],
    "Apple": ["iPhone 11", "iPhone 12 Pro", "iPhone 13 Pro Max", "iPhone 14"],
    "Xiaomi": ["Redmi Note 12", "Mi 11 Lite", "Poco X5", "Redmi K40"],
    "Oppo": ["Reno 8", "Find X5", "A96", "F19 Pro"],
    "Vivo": ["V27 Pro", "Y21s", "X80", "Y75"],
    "Huawei": ["P40 Pro", "Mate 40", "Nova 9", "Y9s"],
    "Realme": ["GT Neo 3", "Narzo 50", "Realme 10", "C35"],
    "OnePlus": ["Nord 2", "OnePlus 9R", "OnePlus 10 Pro"],
    "Infinix": ["Hot 30", "Zero Ultra", "Note 12 Pro"],
}

# === 3. Ambil fraud types dari file Excel kamu ===
fraud_types = pd.read_excel("fraud_types.xlsx")["fraud_type"].dropna().tolist()

# === 4. Tambahin kolom baru ke dataset lama ===
brands = []
models = []
frauds = []

for _ in range(len(df)):
    brand = random.choice(list(device_options.keys()))
    model = random.choice(device_options[brand])
    fraud = random.choice(fraud_types)

    brands.append(brand)
    models.append(model)
    frauds.append(fraud)

df["device_brand"] = brands
df["device_model"] = models
df["fraud_type"] = frauds

# === 5. Simpan hasil ===
df.to_csv("Fraudulent_E_Commerce_Transaction_Data_Updated.csv", index=False)
print("Dataset baru berhasil dibuat!")

