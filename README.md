Real-Time Fraud Detection System

Sistem deteksi penipuan transaksi kartu kredit berbasis streaming yang dirancang untuk memberikan keputusan klasifikasi secara real-time. Proyek ini mengintegrasikan pemrosesan Big Data, infrastruktur messaging berkecepatan tinggi, dan model machine learning yang dioptimalkan untuk menjaga stabilitas risiko perbankan.

Overview

Sistem ini mensimulasikan alur kerja perbankan modern:


Producer: Mensimulasikan transaksi nasabah secara kontinu.
Streaming Pipeline: Menggunakan Apache Kafka untuk menangani aliran data real-time.
Detection Engine: Model XGBoost yang dilatih untuk mendeteksi anomali penipuan (Fraud).
Monitoring: Pencatatan otomatis keputusan sistem ke dalam database log (CSV) untuk keperluan audit dan visualisasi.


Pipeline Architecture

graph LR
    A[Data Source] --> B(Producer)
    B --> C{Kafka Topics}
    C --> D(Consumer + AI Model)
    D --> E[Dashboard/Log]

Dataset

Proyek ini menggunakan dataset transaksi kartu kredit yang sudah melalui proses feature engineering.


Sumber dataset asli: <!-- TODO: isi link/nama dataset, misal Kaggle Credit Card Fraud Dataset -->
File yang dibutuhkan: fraudTrain_engineered.parquet



File .parquet ini tidak disertakan di repository ini karena ukurannya besar. Silakan download dataset asli dari sumber di atas, lalu jalankan script feature engineering (atau train_model.py, jika mencakup proses tersebut) untuk menghasilkan file fraudTrain_engineered.parquet sebelum menjalankan kafka_producer.py.



Installation & Setup

Pastikan Anda telah menginstal Docker Desktop dan Python 3.x.

1. Clone Repository

bashgit clone https://github.com/GalFoks/<nama-repo-anda>.git
cd <nama-repo-anda>

2. Setup Virtual Environment

bashpython -m venv myvenv
source myvenv/bin/activate  # atau myvenv\Scripts\activate di Windows
python -m pip install -r requirements.txt

3. Jalankan Infrastruktur Kafka

bashdocker-compose up -d


Pastikan file docker-compose.yml tersedia di root project. File ini mendefinisikan service Kafka dan Zookeeper yang dibutuhkan sistem.



Configuration (Opsional)

Secara default, kafka_producer.py dan kafka_consumer.py terhubung ke Kafka di localhost:9092.

Untuk menggunakan server Kafka lain (misalnya saat deployment), set environment variable berikut sebelum menjalankan script:

bash# Linux / macOS
export KAFKA_BOOTSTRAP_SERVER=alamat_server:9092

# Windows (PowerShell)
$env:KAFKA_BOOTSTRAP_SERVER="alamat_server:9092"

Execution Instructions

Jalankan sistem dalam urutan berikut:

1. Start Detection System

bashpython kafka_consumer.py

2. Start Transaction Simulation

Buka terminal baru, lalu jalankan:

bashpython kafka_producer.py

Key Features & Performance


Optimized Recall (82%): Model XGBoost dikalibrasi menggunakan scale_pos_weight untuk memastikan penipuan dapat terdeteksi dengan tingkat sensitivitas tinggi.
Feature Engineering: Memanfaatkan Time-Series Features (trans_hour, trans_day) untuk meningkatkan akurasi pendeteksian anomali.
Efficient Risk Mitigation: Mengurangi False Positives secara drastis melalui kalibrasi bobot, yang secara langsung menekan biaya operasional penanganan komplain nasabah.


Project Structure

FileDeskripsitrain_model.pySkrip untuk melatih dan mengoptimasi model AI.kafka_producer.pySimulator aplikasi transaksi perbankan.kafka_consumer.pyBackend AI yang melakukan deteksi real-time.visualize_log.pySkrip untuk menghasilkan visualisasi performa sistem.model_features.pklDaftar fitur yang digunakan model saat training & inference.requirements.txtDaftar dependency Python yang dibutuhkan.

<!-- TODO: konfirmasi nama file model terlatih — apakah fraud_model.pkl ada di repo, atau modelnya tersimpan dengan nama lain? -->
License

Proyek ini menggunakan lisensi MIT — lihat file LICENSE untuk detail lengkap.
