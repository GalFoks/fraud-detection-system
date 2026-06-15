import pandas as pd
from kafka import KafkaConsumer
import json
import joblib
import warnings
import csv
import os

warnings.filterwarnings('ignore')

print("1. Memuat Model Machine Learning...")
model = joblib.load("fraud_model.pkl")
features = joblib.load("model_features.pkl")

# --- PERSIAPAN DATABASE SEDERHANA (CSV LOG) ---
csv_filename = "fraud_monitoring_log.csv"
file_exists = os.path.isfile(csv_filename)

# Membuat file dan header jika belum ada
if not file_exists:
    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['trans_timestamp', 'cc_num', 'amt', 'prediction', 'status'])
print(f"2. Log database siap: {csv_filename}")

print("3. Menghubungkan ke Kafka Server...")
consumer = KafkaConsumer(
    'fraud_transactions',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='latest'
)

print("✅ SISTEM DETEKSI & PENCATATAN AKTIF! Menunggu aliran transaksi...\n")
print("=" * 60)

try:
    for message in consumer:
        transaction = message.value
        
        # Ekstraksi fitur untuk prediksi
        df_trans = pd.DataFrame([transaction])
        
        if 'trans_timestamp' in df_trans.columns:
            df_trans['trans_timestamp'] = pd.to_datetime(df_trans['trans_timestamp'])
            df_trans['trans_hour'] = df_trans['trans_timestamp'].dt.hour
            df_trans['trans_day'] = df_trans['trans_timestamp'].dt.dayofweek
        
        for col in features:
            if col not in df_trans.columns or pd.isna(df_trans[col].iloc[0]):
                df_trans[col] = 0.0
                
        X_live = df_trans[features]
        
        # Lakukan Prediksi
        prediction = model.predict(X_live)[0]
        
        # --- PENCATATAN KE DATABASE (CSV) ---
        timestamp_str = transaction.get('trans_timestamp')
        cc_num = transaction.get('cc_num')
        amt = transaction.get('amt')
        
        if prediction == 1:
            status_text = "BLOKIR (FRAUD)"
            print(f"🚨 [{status_text}] CC: {cc_num} | Nominal: ${amt} | Waktu: {timestamp_str}")
        else:
            status_text = "LOLOS (AMAN)"
            print(f"✅ [{status_text}] CC: {cc_num} | Nominal: ${amt}")
            
        # Menyimpan baris data secara real-time ke file CSV
        with open(csv_filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp_str, cc_num, amt, prediction, status_text])
            
except KeyboardInterrupt:
    print("\n🛑 Sistem Deteksi dimatikan.")
finally:
    consumer.close()