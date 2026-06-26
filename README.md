# Real-Time Fraud Detection System

Sistem deteksi penipuan transaksi kartu kredit berbasis streaming yang dirancang untuk memberikan keputusan klasifikasi secara real-time. Proyek ini mengintegrasikan pemrosesan Big Data, infrastruktur messaging berkecepatan tinggi, dan model machine learning yang dioptimalkan untuk menjaga stabilitas risiko perbankan.

## Overview

Sistem ini mensimulasikan alur kerja perbankan modern:

- **Producer**: Mensimulasikan transaksi nasabah secara kontinu.
- **Streaming Pipeline**: Menggunakan Apache Kafka untuk menangani aliran data real-time.
- **Detection Engine**: Model XGBoost yang dilatih untuk mendeteksi anomali penipuan (Fraud).
- **Monitoring**: Pencatatan otomatis keputusan sistem ke dalam database log (CSV) untuk keperluan audit dan visualisasi.

## Pipeline Architecture

```
graph LR
    A[Data Source] --> B(Producer)
    B --> C{Kafka Topics}
    C --> D(Consumer + AI Model)
    D --> E[Dashboard/Log]
```

## Dataset & Data Pipeline

Proyek ini menggunakan dataset **[Credit Card Transactions Fraud Detection Dataset](https://www.kaggle.com/datasets/kartik2112/fraud-detection)** dari Kaggle (disimulasikan menggunakan tool Sparkov).

> File dataset mentah (`fraudTrain.csv`, `fraudTest.csv`) dan file `.parquet` hasil olahan **tidak disertakan** di repository ini karena ukurannya besar. Silakan download dataset dari link di atas, lalu jalankan tahapan berikut secara berurutan untuk menghasilkan file yang dibutuhkan oleh `kafka_producer.py` dan `train_model.py`.

### Tahapan Data Pipeline

| Tahap | Script | Input | Output |
|---|---|---|---|
| 1. Optimasi & Konversi | `ubahukurandata.py` | `fraudTrain.csv`, `fraudTest.csv` | `fraudTrain_optimized.parquet`, `fraudTest_optimized.parquet` |
| 2. Feature Engineering | `Feature_Engineering.py` *(PySpark)* | `fraudTrain_optimized.parquet` | `fraudTrain_engineered.parquet` |
| 3. Training Model | `train_model.py` | `fraudTrain_engineered.parquet` | `fraud_model.pkl`, `model_features.pkl` |

**Detail tiap tahap:**

1. **`ubahukurandata.py`** — Downcasting tipe data (`int64`/`float64` ke tipe yang lebih kecil) dan mengubah kolom teks berulang (`merchant`, `category`, `gender`, `city`, `state`, `job`) menjadi tipe `category`, lalu menyimpan hasil sebagai Parquet untuk menghemat RAM & ukuran file.
   ```bash
   python ubahukurandata.py
   ```

2. **`Feature_Engineering.py`** — Menghitung fitur tambahan menggunakan PySpark: `distance_km` (jarak geografis nasabah-merchant via haversine formula) dan *velocity features* (`trans_count_1h`, `amt_sum_1h`, dll) menggunakan Spark Window function per `cc_num`. Membutuhkan PySpark terinstal.
   ```bash
   python Feature_Engineering.py
   ```

3. **`train_model.py`** — Melatih model XGBoost dan menyimpan model + daftar fitur. Lihat bagian [Execution Instructions](#execution-instructions) di bawah untuk menjalankan training secara penuh.

> **Catatan:** Pastikan setiap script dijalankan di folder yang sama dengan file data yang dibutuhkan, karena path file di dalam script bersifat relatif (tanpa folder `data/`).

## Installation & Setup

Pastikan Anda telah menginstal **Docker Desktop** dan **Python 3.x**.

### 1. Clone Repository

```bash
git clone https://github.com/GalFoks/fraud-detection-system.git
cd fraud-detection-system
```

### 2. Setup Virtual Environment

```bash
python -m venv myvenv
source myvenv/bin/activate  # atau myvenv\Scripts\activate di Windows
python -m pip install -r requirements.txt
```

### 3. Jalankan Infrastruktur Kafka

```bash
docker-compose up -d
```

> Pastikan file `docker-compose.yml` tersedia di root project. File ini mendefinisikan service Kafka dan Zookeeper yang dibutuhkan sistem.

## Configuration (Opsional)

Secara default, `kafka_producer.py` dan `kafka_consumer.py` terhubung ke Kafka di `localhost:9092`.

Untuk menggunakan server Kafka lain (misalnya saat deployment), set environment variable berikut sebelum menjalankan script:

```bash
# Linux / macOS
export KAFKA_BOOTSTRAP_SERVER=alamat_server:9092

# Windows (PowerShell)
$env:KAFKA_BOOTSTRAP_SERVER="alamat_server:9092"
```

## Execution Instructions

> Pastikan tahapan [Data Pipeline](#dataset--data-pipeline) di atas sudah dijalankan terlebih dahulu, sehingga `fraud_model.pkl`, `model_features.pkl`, dan `fraudTrain_engineered.parquet` sudah tersedia.

Jalankan sistem dalam urutan berikut:

### 1. (Jika belum) Latih Model

```bash
python train_model.py
```

### 2. Start Detection System

```bash
python kafka_consumer.py
```

### 3. Start Transaction Simulation

Buka terminal baru, lalu jalankan:

```bash
python kafka_producer.py
```

## Key Features & Performance

- **Optimized Recall (82%)**: Model XGBoost dikalibrasi menggunakan `scale_pos_weight` untuk memastikan penipuan dapat terdeteksi dengan tingkat sensitivitas tinggi.
- **Feature Engineering**: Memanfaatkan Time-Series Features (`trans_hour`, `trans_day`) untuk meningkatkan akurasi pendeteksian anomali.
- **Efficient Risk Mitigation**: Mengurangi False Positives secara drastis melalui kalibrasi bobot, yang secara langsung menekan biaya operasional penanganan komplain nasabah.

## Project Structure

| File | Deskripsi |
|---|---|
| `ubahukurandata.py` | Optimasi tipe data & konversi CSV mentah ke Parquet. |
| `Feature_Engineering.py` | Feature engineering (PySpark): jarak geografis & velocity features. |
| `train_model.py` | Skrip untuk melatih dan mengoptimasi model AI. |
| `kafka_producer.py` | Simulator aplikasi transaksi perbankan. |
| `kafka_consumer.py` | Backend AI yang melakukan deteksi real-time. |
| `visualize_log.py` | Skrip untuk menghasilkan visualisasi performa sistem. |
| `fraud_model.pkl` | Model XGBoost yang sudah dilatih (output dari `train_model.py`). |
| `model_features.pkl` | Daftar fitur yang digunakan model saat training & inference. |
| `requirements.txt` | Daftar dependency Python yang dibutuhkan. |

