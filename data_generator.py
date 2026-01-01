import requests
import time
import psutil  
import random
import uuid

# Konfigurasi URL API (Sesuaikan port jika berbeda)
API_URL = "http://127.0.0.1:8000/metrics/"

# Daftar nama service pura-pura (Microservices simulation)
SERVICES = ["payment-service", "order-service", "auth-service", "inventory-service"]

def generate_and_send_metrics():
    print(f"🚀 Memulai Data Generator ke {API_URL}...")
    print("Tekan CTRL+C untuk berhenti.\n")

    while True:
        try:
            # 1. AMBIL DATA REAL DARI LAPTOP (CPU & RAM)
            # cpu_percent(interval=1) akan menunggu 1 detik untuk menghitung rata-rata
            real_cpu = psutil.cpu_percent(interval=1)
            real_memory = psutil.virtual_memory().percent

            # 2. SIMULASI DATA LAINNYA
            # Pilih nama service secara acak
            chosen_service = random.choice(SERVICES)
            
            # Simulasi Latency: Semakin tinggi CPU, biasanya latency makin tinggi
            base_latency = random.randint(10, 50)
            if real_cpu > 50:
                base_latency += random.randint(100, 500) # Simulasi lag jika CPU panas
            
            # Simulasi Error: Kadang-kadang terjadi error (10% kemungkinan)
            # Ganti 0.1 menjadi 0.5
            error_val = 1 if random.random() < 0.5 else 0

            # 3. BUAT PAYLOAD (Sesuai model SendData di api.py kamu)
            # Penting: Kita harus generate id_data unik karena di API kamu itu Primary Key manual
            unique_id = str(uuid.uuid4())[:8] # Contoh: 'a1b2c3d4'

            payload = {
                "id_data": unique_id,
                "service_name": chosen_service,
                "cpu_usage": real_cpu,
                "memory_usage": real_memory,
                "latency": base_latency,
                "error_count": error_val
            }

            # 4. KIRIM REQUEST POST KE API
            response = requests.post(API_URL, json=payload)

            # 5. CEK RESPON
            if response.status_code == 201:
                print(f"✅ [Sukses] {chosen_service} | ID: {unique_id} | CPU: {real_cpu}% | Mem: {real_memory}%")
            else:
                print(f"❌ [Gagal] Status: {response.status_code} | Detail: {response.text}")

        except requests.exceptions.ConnectionError:
            print("⚠️ [Error Koneksi] Pastikan api.py sudah dijalankan (uvicorn api:app --reload)")
            time.sleep(2)
        except Exception as e:
            print(f"⚠️ [Error Lain] {e}")
            time.sleep(1)

if __name__ == "__main__":
    generate_and_send_metrics()