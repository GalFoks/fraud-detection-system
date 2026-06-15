import pandas as pd
from kafka import KafkaProducer
import json
import time

# 1. Konfigurasi Kafka Producer
print("Menghubungkan ke Server Kafka...")
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'], # Alamat server Docker Anda
    value_serializer=lambda v: json.dumps(v).encode('utf-8') # Mengubah data menjadi format JSON
)

# Nama jalur/topik tempat data akan mengalir
topic_name = 'fraud_transactions'

# 2. Muat Data
print("Memuat file fraudTrain_engineered.parquet...")
# Kita menggunakan Pandas karena sangat efisien untuk membaca dan mengirim baris per baris
df = pd.read_parquet("fraudTrain_engineered.parquet")

print(f"✅ Siap! Mulai menembakkan data ke topik: '{topic_name}'...")
print("Tekan Ctrl+C di terminal untuk menghentikan simulasi.\n")
print("-" * 50)

try:
    # 3. Simulasi Streaming Data (Baris per baris)
    for index, row in df.iterrows():
        # Ubah satu baris data menjadi format kamus (dictionary)
        transaction = row.to_dict()
        
        # Format waktu perlu diubah ke teks murni (string) agar bisa dikonversi ke JSON
        if 'trans_timestamp' in transaction:
            transaction['trans_timestamp'] = str(transaction['trans_timestamp'])
            
        # Tembakkan data ke Kafka!
        producer.send(topic_name, value=transaction)
        
        # Tampilkan di layar agar kita bisa melihat datanya mengalir
        status_fraud = "🚨 FRAUD" if transaction['is_fraud'] == 1 else "✅ AMAN"
        print(f"[{transaction['trans_timestamp']}] CC: {transaction['cc_num']} | Nominal: ${transaction['amt']} | Status: {status_fraud}")
        
        # Beri jeda waktu 0.5 detik per transaksi agar terasa seperti dunia nyata
        # (Ubah angkanya menjadi lebih kecil jika ingin aliran datanya lebih cepat)
        time.sleep(0.5)

except KeyboardInterrupt:
    print("\n🛑 Simulasi dihentikan secara manual oleh pengguna.")
finally:
    # Tutup koneksi dengan rapi
    producer.flush()
    producer.close()

    print("Koneksi Kafka Producer ditutup.")

    