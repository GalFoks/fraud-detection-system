from pyspark.sql import SparkSession
from pyspark.sql.functions import col, cos, asin, sqrt
from pyspark.sql.window import Window
import pyspark.sql.functions as F

# 1. Inisialisasi Spark Session
spark = SparkSession.builder \
    .appName("FraudDetection_FeatureEngineering") \
    .config("spark.sql.execution.arrow.pyspark.enabled", "true") \
    .getOrCreate()

# 2. Muat Data Parquet
print("Memuat file Parquet...")
df_train = spark.read.parquet("fraudTrain_optimized.parquet")
# Catatan: fraudTest_optimized.parquet tidak dimuat di sini karena belum diproses
# di pipeline ini. Jika dibutuhkan untuk evaluasi, ulangi langkah 3-7 untuk df_test.

# 3. Feature Engineering: Jarak Geospasial (Haversine Formula)
def haversine_distance(lat1, lon1, lat2, lon2):
    r = 6371  # Radius bumi dalam kilometer
    p = 3.141592653589793 / 180
    a = 0.5 - cos((lat2 - lat1) * p) / 2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
    return 2 * r * asin(sqrt(a))

df_train = df_train.withColumn("distance_km",
    haversine_distance(col("lat"), col("long"), col("merch_lat"), col("merch_long")))

# 4. Feature Engineering: Persiapan Waktu (Timestamp)
# Mengubah trans_date_trans_time menjadi tipe Timestamp yang dikenali Spark
df_train = df_train.withColumn("trans_timestamp", col("trans_date_trans_time").cast("timestamp"))

df_train.select("cc_num", "amt", "distance_km", "trans_timestamp", "is_fraud").show(5)

# 5. Feature Engineering Lanjutan: Velocity Features (Agregasi Time-Window)
print("Menghitung fitur Velocity (1 Jam & 24 Jam terakhir)...")

# Kita harus mengubah timestamp menjadi detik (tipe Long) untuk melakukan perhitungan range jendela waktu
df_train = df_train.withColumn("trans_timestamp_long", F.col("trans_timestamp").cast("long"))

# Mendefinisikan Window (Jendela Waktu)
# Dikelompokkan per kartu kredit (cc_num), diurutkan berdasarkan waktu
# rangeBetween(-3600, -1) artinya: dari 3600 detik (1 jam) yang lalu HINGGA SEBELUM transaksi ini
# (offset -1 mengecualikan transaksi saat ini sendiri, agar tidak terjadi data leakage)
w_1h = Window.partitionBy("cc_num").orderBy("trans_timestamp_long").rangeBetween(-3600, -1)

# rangeBetween(-86400, -1) artinya: dalam 24 jam terakhir, tidak termasuk transaksi saat ini
w_24h = Window.partitionBy("cc_num").orderBy("trans_timestamp_long").rangeBetween(-86400, -1)

# Menerapkan window ke dataframe
df_train = df_train.withColumn("trans_count_1h", F.count("trans_num").over(w_1h)) \
                   .withColumn("amt_sum_1h", F.sum("amt").over(w_1h)) \
                   .withColumn("trans_count_24h", F.count("trans_num").over(w_24h)) \
                   .withColumn("amt_sum_24h", F.sum("amt").over(w_24h))

# Isi NULL dengan 0 untuk transaksi pertama suatu kartu (belum ada riwayat di window)
df_train = df_train.fillna(0, subset=["trans_count_1h", "amt_sum_1h", "trans_count_24h", "amt_sum_24h"])

# 6. Tampilkan Hasil Fitur Baru
print("Hasil Ekstraksi Fitur Velocity:")
df_train.select("cc_num", "amt", "trans_timestamp", "trans_count_1h", "amt_sum_1h", "is_fraud").show(10)

# 7. Mengurutkan Data Secara Kronologis & Menyimpan untuk Simulasi Kafka
# Untuk simulasi streaming yang realistis, data HARUS diurutkan berdasarkan waktu dari terlama ke terbaru
print("Mengurutkan data dan menyimpan hasil rekayasa fitur...")
df_train_sorted = df_train.orderBy("trans_timestamp_long")

# Kita simpan hasil akhir ini ke file Parquet baru agar Kafka Producer tinggal membacanya
df_train_sorted.write.mode("overwrite").parquet("fraudTrain_engineered.parquet")

print("✅ Pipeline Feature Engineering Selesai! Data siap untuk disimulasikan sebagai Stream.")

# 8. Tutup Spark Session dengan rapi
spark.stop()

