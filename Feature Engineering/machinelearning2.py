# ==========================================
# DETEKSI FRAUD TRANSAKSI E-COMMERCE
# Menggunakan Naive Bayes & Random Forest
# ==========================================

# 1. Import library yang dibutuhkan
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay

# 2. Baca dataset
df = pd.read_csv('Fraudulent_E-Commerce_Transaction_Data.csv')

# 3. Pilih fitur numerik yang relevan & target
features = ['Transaction Amount', 'Quantity', 'Customer Age', 'Transaction Hour', 'Account Age Days']
X = df[features].fillna(0) # isi NaN jika ada
y = df['Is Fraudulent'] # target: 0 = normal, 1 = fraud

# 4. Bagi data menjadi data latih dan uji
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42)

# 5. Standarisasi data (penting untuk Naive Bayes & model lainnya)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 6. Definisikan model yang akan digunakan
models = {
    "Naive Bayes": GaussianNB(),
    "Random Forest": RandomForestClassifier(random_state=42)
}

# 7. Latih dan evaluasi masing-masing model
for name, model in models.items():
    print(f"\n📌 Model: {name}")
    
    # Latih model
    model.fit(X_train_scaled, y_train)
    
    # Prediksi
    y_pred = model.predict(X_test_scaled)
    
    # Laporan performa klasifikasi
    print("Classification Report:")
    print(classification_report(y_test, y_pred, digits=3))
    
    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Normal', 'Fraud'])
    disp.plot(cmap='Blues')
    plt.title(f'Confusion Matrix: {name}')
    plt.show()
