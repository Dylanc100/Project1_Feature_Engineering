import pandas as pd

# 1. BACA FILE CSV
df = pd.read_csv('dummy_ecommerce_fraud_dataset.csv')
print("5 data teratas:")
print(df.head())

# 2. KONVERSI KOLOM WAKTU
df['signup_time'] = pd.to_datetime(df['signup_time'])
df['purchase_time'] = pd.to_datetime(df['purchase_time'])

# 3. FEATURE ENGINEERING

# Fitur 1: Selisih waktu signup ke transaksi (dalam jam)
df['time_since_signup'] = (df['purchase_time'] - df['signup_time']).dt.total_seconds() / 3600

# Fitur 2: Selang waktu antar transaksi user (dalam menit)
df = df.sort_values(['user_id', 'purchase_time'])
df['prev_time'] = df.groupby('user_id')['purchase_time'].shift(1)
df['purchase_interval'] = (df['purchase_time'] - df['prev_time']).dt.total_seconds() / 60

# Fitur 3: Perubahan IP
df['prev_ip'] = df.groupby('user_id')['ip_address'].shift(1)
df['ip_change_flag'] = (df['ip_address'] != df['prev_ip']).astype(int)

# Fitur 4: Rata-rata nilai transaksi per user
df['avg_purchase_value'] = df.groupby('user_id')['purchase_value'].transform('mean')

# Fitur 5: Berapa kali kode promo digunakan
df['promo_usage_count'] = df['promo_code'].map(df['promo_code'].value_counts())

# 4. TAMPILKAN HASILNYA
print("\nData setelah feature engineering:")
print(df[['user_id', 'purchase_value', 'time_since_signup', 'purchase_interval', 'ip_change_flag', 'avg_purchase_value', 'promo_usage_count']].head())

# 5. SIMPAN KE FILE BARU
df.to_csv('hasil_feature_engineering.csv', index=False)
print("\n File hasil_feature_engineering.csv berhasil disimpan")
