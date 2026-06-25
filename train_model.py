
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
