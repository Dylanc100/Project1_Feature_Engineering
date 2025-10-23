import pandas as pd

# 1. Baca dataset
df = pd.read_csv("Fraudulent_E-Commerce_Transaction_Data.csv")

# 2. Bersihkan nama kolom: lowercase + strip spasi
df.columns = df.columns.str.lower().str.strip()

# 3. Gabungkan tanggal dan jam transaksi
df['transaction_datetime'] = pd.to_datetime(df['transaction date']) + pd.to_timedelta(df['transaction hour'], unit='h')

# 4. Tambahkan rules fraud:
df['rule_high_amount'] = df['transaction amount'] > 1_000_000
df['rule_night_time'] = df['transaction hour'].between(0, 5)
df['rule_old_account'] = df['account age days'] < 30  # akun terlalu baru
df['rule_mismatch_location'] = df['shipping address'] != df['billing address']

# 5. Hitung berapa rule yang terpenuhi
df['total_rules_triggered'] = df[
    ['rule_high_amount', 'rule_night_time', 'rule_old_account', 'rule_mismatch_location']
].sum(axis=1)

# 6. Tandai sebagai suspicious jika ada rule terpenuhi
df['is_suspicious'] = df['total_rules_triggered'] > 0

# 7. Tampilkan data mencurigakan
suspicious = df[df['is_suspicious'] == True]
print("Transaksi mencurigakan berdasarkan rules:")
print(suspicious[['transaction id', 'transaction amount', 'transaction_datetime', 
                  'account age days', 'shipping address', 'billing address',
                  'total_rules_triggered']].head())

# (Opsional) Simpan hasil ke file
suspicious.to_csv("suspicious_transactions.csv", index=False)



