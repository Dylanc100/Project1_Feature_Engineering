import csv
import random
import faker
from datetime import datetime, timedelta

# Inisialisasi Faker
fake = faker.Faker()

# Tentukan jumlah data
n_fraud = 1200   # minimal 1000 fraud
n_nonfraud = 1200  # minimal 1000 non-fraud
total = n_fraud + n_nonfraud

# Nama file CSV
filename = "fraudulent_transactions.csv"

# Header kolom
fields = [
    "TransactionID", "CustomerID", "TransactionType", "TransactionAmount",
    "TransactionDate", "TransactionTime", "IP_Location", "Device",
    "OldBalance", "NewBalance", "SenderAccount", "ReceiverAccount",
    "SenderLocation", "ReceiverLocation", "SenderBank", "ReceiverBank", "isFraud"
]

# Tipe transaksi
transaction_types = ["Transfer", "Payment", "Withdrawal", "Deposit"]

# Nama bank dummy
banks = ["Bank A", "Bank B", "Bank C", "Bank D", "Bank E"]

# Generate data
rows = []
for i in range(total):
    isfraud = 1 if i < n_fraud else 0
    transaction_id = f"T{i+1:06d}"
    customer_id = f"C{random.randint(1000, 9999)}"
    transaction_type = random.choice(transaction_types)
    amount = round(random.uniform(10, 10000), 2)

    # Balance lama dan baru
    old_balance = round(random.uniform(100, 20000), 2)
    if isfraud:
        new_balance = old_balance - random.uniform(0, amount)  # fraud sering mismatch
    else:
        new_balance = old_balance - amount if old_balance >= amount else old_balance

    # Date & Time
    transaction_date = fake.date_between(start_date="-1y", end_date="today")
    transaction_time = fake.time(pattern="%H:%M:%S")

    # Sender & Receiver
    sender_account = f"AC{random.randint(100000, 999999)}"
    receiver_account = f"AC{random.randint(100000, 999999)}"
    sender_location = fake.city()
    receiver_location = fake.city()
    sender_bank = random.choice(banks)
    receiver_bank = random.choice(banks)

    row = [
        transaction_id, customer_id, transaction_type, amount,
        transaction_date, transaction_time, fake.ipv4(), fake.user_agent(),
        old_balance, round(new_balance, 2), sender_account, receiver_account,
        sender_location, receiver_location, sender_bank, receiver_bank, isfraud
    ]
    rows.append(row)

# Simpan ke CSV
with open(filename, "w", newline="", encoding="utf-8") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(fields)
    csvwriter.writerows(rows)

print(f"✅ Dataset berhasil dibuat dan disimpan ke file: {filename}")





