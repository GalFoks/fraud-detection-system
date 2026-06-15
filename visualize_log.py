import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

print("1. Membaca database CSV...")
df = pd.read_csv("fraud_monitoring_log.csv")

# Mengubah teks waktu menjadi format waktu yang bisa dibaca grafik
df['trans_timestamp'] = pd.to_datetime(df['trans_timestamp'])

# Memisahkan data berdasarkan status prediksi
df_aman = df[df['prediction'] == 0]
df_fraud = df[df['prediction'] == 1]

print("2. Merancang grafik visual...")
# Membuat kanvas grafik dengan rasio layar presentasi (16:9)
fig, ax = plt.subplots(figsize=(10, 5.625))

# Menggambar titik data transaksi aman (warna hijau/abu yang kalem)
ax.scatter(df_aman['trans_timestamp'], df_aman['amt'], 
           color='#2ca02c', alpha=0.5, label='Lolos (Aman)', edgecolors='white', s=50)

# Menggambar titik data fraud (warna merah tegas dengan simbol X besar)
ax.scatter(df_fraud['trans_timestamp'], df_fraud['amt'], 
           color='#d62728', alpha=1.0, label='Blokir (Fraud)', edgecolors='black', s=120, marker='X')

# Format tampilan agar terlihat profesional, bersih, dan akademis
ax.set_title('Real-Time Fraud Detection Monitoring', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Waktu Transaksi', fontsize=11, fontweight='bold')
ax.set_ylabel('Nominal Transaksi (USD)', fontsize=11, fontweight='bold')

# Merapikan format jam di sumbu X
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
plt.xticks(rotation=45)

# Menambahkan garis bantu (grid) yang tipis dan tidak mengganggu
ax.grid(True, linestyle='--', alpha=0.5)

# Menambahkan legenda (keterangan) di sudut yang aman
ax.legend(loc='upper left', frameon=True, shadow=True)

# Memastikan layout tidak terpotong saat disimpan
plt.tight_layout()

print("3. Menyimpan grafik resolusi tinggi...")
plt.savefig('fraud_dashboard.png', dpi=300)

print("✅ SUKSES! Visualisasi telah disimpan sebagai 'fraud_dashboard.png'.")