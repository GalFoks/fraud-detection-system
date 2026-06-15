Real-Time Fraud Detection System
Sistem deteksi penipuan transaksi kartu kredit berbasis streaming yang dirancang untuk memberikan keputusan klasifikasi secara real-time. Proyek ini mengintegrasikan pemrosesan Big Data, infrastruktur messaging berkecepatan tinggi, dan model machine learning yang dioptimalkan untuk menjaga stabilitas risiko perbankan.

Overview
Sistem ini mensimulasikan alur kerja perbankan modern:

Producer: Mensimulasikan transaksi nasabah secara kontinu.

Streaming Pipeline: Menggunakan Apache Kafka untuk menangani aliran data real-time.

Detection Engine: Model XGBoost yang dilatih untuk mendeteksi anomali penipuan (Fraud).

Monitoring: Pencatatan otomatis keputusan sistem ke dalam database log (CSV) untuk keperluan audit dan visualisasi.

Pipeline Architecture
Cuplikan kode
graph LR
    A[Data Source] --> B(Producer)
    B --> C{Kafka Topics}
    C --> D(Consumer + AI Model)
    D --> E[Dashboard/Log]
Installation & Setup
Pastikan Anda telah menginstal Docker Desktop dan Python 3.x.

Clone Repository:

Bash
git clone [link-repo-anda]
cd latihan_2
Setup Virtual Environment:

Bash
python -m venv myvenv
source myvenv/bin/activate  # atau myvenv\Scripts\activate di Windows
python -m pip install -r requirements.txt
Infrastruktur:
Jalankan server Kafka:

Bash
docker-compose up -d
Execution Instructions
Jalankan sistem dalam urutan berikut:

Start Detection System:

Bash
python kafka_consumer.py
Start Transaction Simulation:
Buka terminal baru, lalu jalankan:

Bash
python kafka_producer.py
Key Features & Performance
Optimized Recall (82%): Model XGBoost dikalibrasi menggunakan scale_pos_weight untuk memastikan penipuan dapat terdeteksi dengan tingkat sensitivitas tinggi.

Feature Engineering: Memanfaatkan Time-Series Features (trans_hour, trans_day) untuk meningkatkan akurasi pendeteksian anomali.

Efficient Risk Mitigation: Mengurangi False Positives secara drastis melalui kalibrasi bobot, yang secara langsung menekan biaya operasional penanganan komplain nasabah.

Project Structure
train_model.py: Skrip untuk melatih dan mengoptimasi model AI.

kafka_producer.py: Simulator aplikasi transaksi perbankan.

kafka_consumer.py: Backend AI yang melakukan deteksi real-time.

visualize_log.py: Skrip untuk menghasilkan visualisasi performa sistem.

fraud_model.pkl: Model Machine Learning yang sudah dilatih.

