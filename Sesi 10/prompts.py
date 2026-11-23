# %% Import Library
from email import message
import os
import ollama


# %% Cell 1: Inisialisasi Client & Model

client = ollama.Client()
MODEL_ID = 'gpt-oss:20b'

# Menyimpan coversation history
messages = []

# Data Ulasan untuk Demo
ulasan = "Pengiriman cepat 1 hari sampai, tapi pas dibuka ternyata layar HP-nya retak."

print("--- DEMO 1: Vague Prompt ---")

prompt_1 = f"Tolong klasifikasikan ulasan pelanggan ini: '{ulasan}'"

messages.append({"role": "user", "content": prompt_1})

# Buat sesi chat
response_1 = client.chat(
    model=MODEL_ID,
    messages=messages,
    options={'temperature': 0.2})

messages.append({"role": "assistant", 
                 "content": response_1.message.content})

print("[PROMPT]")
print(prompt_1)
print("\n[HASIL MODEL]")
print(response_1.message.content)

print("\n--- DEMO 2: Task & Format Optimization ---")

prompt_2 = f"""
Klasifikasikan ulasan pelanggan ke dalam salah satu kategori berikut:
- pengiriman
- kualitas produk
- pelayanan
- harga

Ulasan: '{ulasan}'

Jawab hanya dengan nama kategorinya saja, gunakan huruf kecil semua, tanpa titik atau tanda baca lainnya.
"""

messages.append({"role": "user", "content": prompt_2})

response_2 = client.chat(
    model=MODEL_ID,
    messages=messages,
    options={'temperature': 0.2})

messages.append({"role": "assistant", 
                 "content": response_2.message.content})

print("[PROMPT]")
print(prompt_2)
print("\n[HASIL MODEL]")
print(response_2.message.content)

print("\n--- DEMO 3: Full 4-Quadrant Framework ---")

prompt_3 = f"""
[PERSONA]
Kamu adalah Senior Customer Care Analyst di perusahaan e-commerce. Kamu sangat teliti dan analitis.

[TASK]
Klasifikasikan ulasan pelanggan ke dalam SATU kategori utama.

[CONTEXT]
Kategori yang tersedia: 'pengiriman', 'kualitas produk', 'pelayanan', 'harga'.
ATURAN KHUSUS: Jika pelanggan memuji pengiriman tetapi mengeluhkan barang rusak/cacat saat diterima, maka fokus utamanya adalah kerusakan barang. Klasifikasikan sebagai 'kualitas produk', BUKAN 'pengiriman'.

[FORMAT]
Berikan jawaban tunggal berupa nama kategori (huruf kecil). Tidak boleh ada teks tambahan.

[INPUT]
Ulasan: '{ulasan}'
"""

# Konfigurasi temperature disisipkan saat pembuatan chat

messages.append({"role": "user", "content": prompt_3})
response_3 = client.chat(
    model=MODEL_ID,
    messages=messages,
    options={'temperature': 0.2}
)

print("[PROMPT]")
print(prompt_3)
print("\n[HASIL MODEL]")
print(response_3.message.content)

# --- DEMO 1: Vague Prompt ---
# [PROMPT]
# Tolong klasifikasikan ulasan pelanggan ini: 'Pengiriman cepat 1 hari sampai, tapi pas dibuka ternyata layar HP-nya retak.'

# [HASIL MODEL]
# Ulasan pelanggan tersebut dapat diklasifikasikan ke dalam beberapa kategori sebagai berikut:

# 1. **Klasifikasi Sentimen:** **Campuran (Mixed)** cenderung **Negatif**
#    * *Alasan:* Ada aspek positif yang dipuji (pengiriman cepat), namun ada aspek negatif yang sangat fatal dan merugikan (layar HP retak saat diterima). Masalah utama (produk rusak) membuat pengalaman keseluruhan menjadi buruk.

# 2. **Klasifikasi Topik / Kategori Masalah:**
#    * **Layanan Pengiriman:** Positif (Cepat, 1 hari sampai).
#    * **Kualitas Produk / Kondisi Barang:** Negatif (Produk rusak/cacat/retak).
#    * **Pengemasan (Packaging):** Kemungkinan buruk atau kurang aman, sehingga menyebabkan layar retak di jalan (atau barang memang sudah rusak sebelum dikirim).

# **Kesimpulan untuk Tim Layanan Pelanggan (Customer Service):**
# Ulasan ini memerlukan **tindak lanjut segera** (retur, pengembalian dana, atau penggantian unit baru) karena pelanggan menerima produk yang cacat fisik, meskipun layanan logistik sudah bekerja dengan baik.

# --- DEMO 2: Task & Format Optimization ---
# [PROMPT]

# Klasifikasikan ulasan pelanggan ke dalam salah satu kategori berikut:
# - pengiriman
# - kualitas produk
# - pelayanan
# - harga

# Ulasan: 'Pengiriman cepat 1 hari sampai, tapi pas dibuka ternyata layar HP-nya retak.'

# Jawab hanya dengan nama kategorinya saja, gunakan huruf kecil semua, tanpa titik atau tanda baca lainnya.


# [HASIL MODEL]
# kualitas produk

# --- DEMO 3: Full 4-Quadrant Framework ---
# [PROMPT]

# [PERSONA]
# Kamu adalah Senior Customer Care Analyst di perusahaan e-commerce. Kamu sangat teliti dan analitis.

# [TASK]
# Klasifikasikan ulasan pelanggan ke dalam SATU kategori utama.

# [CONTEXT]
# Kategori yang tersedia: 'pengiriman', 'kualitas produk', 'pelayanan', 'harga'.
# ATURAN KHUSUS: Jika pelanggan memuji pengiriman tetapi mengeluhkan barang rusak/cacat saat diterima, maka fokus utamanya adalah kerusakan barang. Klasifikasikan sebagai 'kualitas produk', BUKAN 'pengiriman'.

# [FORMAT]
# Berikan jawaban tunggal berupa nama kategori (huruf kecil). Tidak boleh ada teks tambahan.

# [INPUT]
# Ulasan: 'Pengiriman cepat 1 hari sampai, tapi pas dibuka ternyata layar HP-nya retak.'


# [HASIL MODEL]
# kualitas produk
# %%
