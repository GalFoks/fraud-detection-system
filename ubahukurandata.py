import pandas as pd
import os
import time

def optimasi_dan_konversi(nama_file_csv):
    # 1. Cek keberadaan file
    if not os.path.exists(nama_file_csv):
        print(f"❌ File {nama_file_csv} tidak ditemukan! Pastikan posisinya satu folder dengan script ini.")
        return

    print(f"\n--- Memproses File: {nama_file_csv} ---")
    waktu_mulai = time.time()
    
    # 2. Muat dataset CSV ke RAM
    print("Mengunduh data ke memori...")
    df = pd.read_csv(nama_file_csv)

    # 3. Hitung ukuran awal (RAM & Hardisk)
    memori_awal = df.memory_usage(deep=True).sum() / (1024 ** 2)
    ukuran_hardisk_awal = os.path.getsize(nama_file_csv) / (1024 ** 2)

    # 4. Proses Optimasi (Downcasting)
    print("Melakukan optimasi memori (downcasting)...")
    
    # A. Optimasi Angka Bulat (Integer)
    for col in df.select_dtypes(include=['int64']).columns:
        df[col] = pd.to_numeric(df[col], downcast='integer')

    # B. Optimasi Angka Desimal (Float)
    for col in df.select_dtypes(include=['float64']).columns:
        df[col] = pd.to_numeric(df[col], downcast='float')

    # C. Optimasi Teks Berulang menjadi 'Category'
    kolom_kategori = ['merchant', 'category', 'gender', 'city', 'state', 'job']
    for col in kolom_kategori:
        if col in df.columns:
            df[col] = df[col].astype('category')

    # 5. Hitung ukuran RAM setelah optimasi
    memori_akhir = df.memory_usage(deep=True).sum() / (1024 ** 2)

    # 6. Simpan ke format Parquet
    nama_file_parquet = nama_file_csv.replace('.csv', '_optimized.parquet')
    print(f"Menyimpan data ke format Parquet ({nama_file_parquet})...")
    df.to_parquet(nama_file_parquet, engine='pyarrow', index=False)

    # 7. Hitung ukuran Hardisk setelah disimpan ke Parquet
    ukuran_hardisk_akhir = os.path.getsize(nama_file_parquet) / (1024 ** 2)
    waktu_selesai = time.time()

    # 8. Tampilkan Laporan
    print(f"✅ Selesai dalam {waktu_selesai - waktu_mulai:.2f} detik!")
    print(f"   🔹 RAM sebelum: {memori_awal:.2f} MB | Sesudah: {memori_akhir:.2f} MB (Hemat {100 - (memori_akhir/memori_awal*100):.1f}%)")
    print(f"   🔹 Ukuran File di Hardisk: Dari {ukuran_hardisk_awal:.2f} MB Menjadi {ukuran_hardisk_akhir:.2f} MB!")

# =====================================================================
# BLOK EKSEKUSI UTAMA
# =====================================================================
if __name__ == "__main__":
    # Mengeksekusi file fraudTrain.csv
    optimasi_dan_konversi('fraudTrain.csv')
    
    # Mengeksekusi file fraudTest.csv
    optimasi_dan_konversi('fraudTest.csv')