# =====================================================
# MACHINE LEARNING UNTUK DETEKSI FRAUD TRANSAKSI
# Dataset dengan csv dummy saya: final_fraud_dataset_with_features.csv
# =====================================================

# 1. Import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

# 2. Baca dataset
df = pd.read_csv('final_fraud_dataset_with_features.csv')

# 3. Tambah label fraud (jika purchase_value > 500000 dianggap fraud)
df['is_fraud'] = df['purchase_value'].apply(lambda x: 1 if x > 500000 else 0)

# 4. Pilih fitur dan target
features = ['time_since_signup', 'purchase_interval', 'ip_change_flag',
            'avg_purchase_value', 'promo_usage_count']
X = df[features].fillna(0)
y = df['is_fraud']

# 5. Split data dan normalisasi
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 6. Definisikan dan latih model
models = {
    "Logistic Regression": LogisticRegression(),
    "Decision Tree": DecisionTreeClassifier(random_state=42),
    "Random Forest": RandomForestClassifier(random_state=42)
}

# 7. Evaluasi setiap model
for name, model in models.items():
    print(f"\n Model: {name}")
    
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)
    
    # Laporan performa
    print(classification_report(y_test, y_pred, digits=3))
    
    # Confusion Matrix (grafik)
    cm = confusion_matrix(y_test, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Normal', 'Fraud'])
    disp.plot(cmap='Blues')
    plt.title(f'Confusion Matrix: {name}')
    plt.show()
