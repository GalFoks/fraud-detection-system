# import pandas as pd
# from xgboost import XGBClassifier
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import classification_report, confusion_matrix
# import joblib

# print("1. Memuat data dari Parquet...")
# df = pd.read_parquet("fraudTrain_engineered.parquet")

# # 2. Menentukan Kolom Fitur (X) dan Target (y)
# # Kita hanya menggunakan angka-angka penting hasil rekayasa PySpark
# features = ['amt', 'distance_km', 'trans_count_1h', 'amt_sum_1h']
# target = 'is_fraud'

# print("2. Membersihkan dan menyiapkan data...")
# # Mengisi nilai kosong (NaN) dengan 0. 
# # Nilai NaN biasanya muncul di transaksi pertama user karena belum ada histori 1 jam sebelumnya.
# df[features] = df[features].fillna(0)

# X = df[features]
# y = df[target]

# # Membagi data: 80% untuk belajar (Training), 20% untuk ujian (Testing)
# # stratify=y memastikan proporsi fraud di training dan testing tetap seimbang
# print("   Membagi data Training dan Testing (80:20)...")
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# print("\n3. Melatih Model XGBoost (Berbasis Tree)...")
# # Mengatur hyperparameter dasar XGBoost
# model = XGBClassifier(
#     n_estimators=100,        # Jumlah "pohon" keputusan
#     max_depth=5,             # Kedalaman maksimal setiap pohon
#     learning_rate=0.1,       # Seberapa cepat model belajar
#     random_state=42,
#     eval_metric='logloss'
# )
# model.fit(X_train, y_train)

# print("\n4. Mengevaluasi Performa Model...")
# y_pred = model.predict(X_test)

# print("-" * 50)
# print("LAPORAN KLASIFIKASI (Classification Report):")
# print(classification_report(y_test, y_pred))

# print("MATRIKS KEBINGUNGAN (Confusion Matrix):")
# print(confusion_matrix(y_test, y_pred))
# print("-" * 50)

# print("\n5. Menyimpan Model ke dalam File...")
# joblib.dump(model, "fraud_model.pkl")

# # Menyimpan daftar nama fitur agar nanti Consumer tidak salah urutan kolom
# joblib.dump(features, "model_features.pkl")

# print("✅ SUKSES! Otak Machine Learning telah disimpan sebagai 'fraud_model.pkl'.")








import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import joblib

print("1. Memuat data dari Parquet...")
df = pd.read_parquet("fraudTrain_engineered.parquet")

print("2. Melakukan Pengayaan Data (Feature Engineering)...")
# Mengubah teks waktu menjadi objek datetime
df['trans_timestamp'] = pd.to_datetime(df['trans_timestamp'])

# Mengekstrak Jam dan Hari
df['trans_hour'] = df['trans_timestamp'].dt.hour
df['trans_day'] = df['trans_timestamp'].dt.dayofweek

# Daftar fitur KINI BERTAMBAH
features = ['amt', 'distance_km', 'trans_count_1h', 'amt_sum_1h', 'trans_hour', 'trans_day']
target = 'is_fraud'

print("3. Membersihkan dan menyiapkan data...")
df[features] = df[features].fillna(0)

X = df[features]
y = df[target]

print("   Membagi data Training dan Testing (80:20)...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

bobot_kalibrasi = 20

print("\n4. Melatih Model XGBoost dengan Fitur Waktu...")
model = XGBClassifier(
    n_estimators=100,
    max_depth=6,             # Kita naikkan sedikit kedalamannya agar bisa mencerna fitur baru
    learning_rate=0.1,
    scale_pos_weight=bobot_kalibrasi,
    random_state=42,
    eval_metric='logloss'
)
model.fit(X_train, y_train)

print("\n5. Mengevaluasi Performa Model Super...")
y_pred = model.predict(X_test)

print("-" * 50)
print("LAPORAN KLASIFIKASI (Classification Report):")
print(classification_report(y_test, y_pred))

print("MATRIKS KEBINGUNGAN (Confusion Matrix):")
print(confusion_matrix(y_test, y_pred))
print("-" * 50)

print("\n6. Menyimpan Model ke dalam File...")
joblib.dump(model, "fraud_model.pkl")
joblib.dump(features, "model_features.pkl")

print("✅ SUKSES! Otak Machine Learning yang Diperkaya telah disimpan.")