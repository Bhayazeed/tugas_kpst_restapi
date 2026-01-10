# Sistem Monitoring Microservice REST API (Tugas KPST)

Proyek ini adalah implementasi sistem monitoring sederhana berbasis **REST API** menggunakan **FastAPI**. Sistem ini dirancang untuk mengumpulkan, menyimpan, dan memantau metrik kinerja (CPU, Memori, Latensi, dan Error Rate) dari berbagai layanan mikro (microservices) simulasi.

Proyek ini terdiri dari dua komponen utama:

1. **API Server (`api.py`)**: Menerima dan menyimpan data metrik ke dalam database SQLite.
2. **Data Generator (`data_generator.py`)**: Mensimulasikan aktivitas microservice dan mengirimkan data dummy secara berkala ke API.

## 📂 Struktur Proyek

Berikut adalah penjelasan singkat mengenai file-file dalam proyek ini:

* `api.py`: Kode utama untuk menjalankan server API (FastAPI). Menangani routing, validasi data, dan koneksi database.
* `data_generator.py`: Skrip simulasi yang menghasilkan data metrik (CPU & RAM real-time dari laptop, serta simulasi latensi) dan mengirimkannya ke API.
* `create_database.py`: Skrip utilitas untuk membuat tabel database SQLite (`data_monitor.db`) secara manual.
* `data_monitor.db`: File database SQLite tempat data metrik disimpan.
* `system_monitor.log`: File log yang mencatat setiap request yang masuk ke API beserta durasi prosesnya.
* `requirements.txt`: Daftar pustaka (library) Python yang dibutuhkan proyek ini.

## 🛠️ Prasyarat (Prerequisites)

Sebelum menjalankan proyek, pastikan Anda telah menginstal:

* **Python 3.10+**
* **PIP** (Python Package Installer)

## 🚀 Cara Instalasi

Ikuti langkah-langkah berikut untuk menyiapkan lingkungan pengembangan:

1. **Clone atau Unduh Repository ini**
Pastikan semua file berada dalam satu folder.
2. **Buat Virtual Environment (Opsional tapi Disarankan)**
Supaya library tidak tercampur dengan sistem global.
```bash
# Untuk Windows
python -m venv venv
venv\Scripts\activate

# Untuk macOS/Linux
python3 -m venv venv
source venv/bin/activate

```


3. **Instal Dependencies**
Instal library yang diperlukan menggunakan `requirements.txt`.
```bash
pip install -r requirements.txt

```


*Catatan: Karena `data_generator.py` menggunakan library tambahan yang mungkin belum ada di `requirements.txt`, jalankan juga perintah berikut:*
```bash
pip install requests psutil

```


4. **Inisialisasi Database**
Jalankan skrip ini untuk membuat file `data_monitor.db` dan tabel yang diperlukan.
```bash
python create_database.py

```



## ⚡ Cara Menjalankan Aplikasi

Anda perlu membuka **dua terminal** berbeda untuk menjalankan sistem ini secara penuh.

### Terminal 1: Menjalankan API Server

Jalankan perintah berikut untuk mengaktifkan server FastAPI:

```bash
fastapi dev api.py
# Atau jika menggunakan uvicorn secara langsung:
uvicorn api:app --reload

```

* Server akan berjalan di: `http://127.0.0.1:8000`
* Dokumentasi interaktif (Swagger UI) dapat diakses di: `http://127.0.0.1:8000/docs`

### Terminal 2: Menjalankan Data Generator

Buka terminal baru (pastikan virtual environment sudah aktif), lalu jalankan:

```bash
python data_generator.py

```

* Script ini akan mulai mengirim data ke server setiap detik.
* Anda akan melihat log output seperti: `✅ [Sukses] payment-service | ID: a1b2c3d4...`

## 📡 Dokumentasi API Endpoints

Berikut adalah daftar endpoint yang tersedia pada sistem ini:

### 1. Cek Kesehatan Sistem

* **URL:** `/health`
* **Method:** `GET`
* **Deskripsi:** Memastikan server berjalan dengan baik.
* **Response:**
```json
{ "message": "Sistem HIDUP ONLINE!" }

```



### 2. Kirim Data Metrik (Ingest)

* **URL:** `/metrics/`
* **Method:** `POST`
* **Deskripsi:** Menerima data metrik baru dari client/generator.
* **Body (JSON):**
```json
{
  "id_data": "unik_id_string",
  "service_name": "order-service",
  "cpu_usage": 45.2,
  "memory_usage": 60.5,
  "latency": 120,
  "error_count": 0
}

```



### 3. Ambil Semua Data Metrik

* **URL:** `/metrics/`
* **Method:** `GET`
* **Deskripsi:** Mengambil seluruh history data metrik yang tersimpan di database.

## 📝 Logging & Monitoring

Sistem ini dilengkapi dengan mekanisme logging ganda (Dual Handler Logging):

1. **Console/Terminal:** Menampilkan log secara real-time saat server berjalan.
2. **File Log (`system_monitor.log`):** Menyimpan riwayat request untuk keperluan audit. Format log mencakup waktu, method, status, dan durasi proses.

Contoh Log:

```text
2026-01-02 02:13:13,247 - INFO - REQUEST: POST /metrics/ - STATUS: 201 - DURATION: 218.35ms

```

## ⚠️ Troubleshooting

* **Error: `ModuleNotFoundError: No module named 'psutil'**`
* Solusi: Jalankan `pip install psutil`.


* **Error: `Connection refused` pada generator**
* Solusi: Pastikan Terminal 1 (API Server) sudah berjalan sebelum menjalankan generator.


* **Database Error / IntegrityError**
* Solusi: Hapus file `data_monitor.db` dan jalankan ulang `python create_database.py` untuk mereset database.
