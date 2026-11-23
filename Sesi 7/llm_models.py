import time
from sentence_transformers import SentenceTransformer
from google import genai

# --- 1. SETUP GEMINI API (SDK TERBARU) ---
# Masukkan API Key melalui parameter atau pastikan environment variable GEMINI_API_KEY sudah di-set
client = genai.Client()

# --- 2. SETUP OPEN SOURCE ---
model_st = SentenceTransformer('all-MiniLM-L6-v2')

# Teks yang akan diuji (Gunakan bahasa Inggris agar sejalan dengan model all-MiniLM-L6-v2)
teks_uji = "This is a sample sentence to test the latency of text embedding models."

print("Mulai pengujian latency...\n")

# --- TEST A: OPEN SOURCE (Lokal) ---
start_time_local = time.time()
emb_local = model_st.encode(teks_uji)
latency_local = time.time() - start_time_local
print(f"✅ Latency Open-Source (all-MiniLM-L6-v2): {latency_local:.4f} detik")

# --- TEST B: API-BASED (Gemini) ---
try:
    start_time_api = time.time()
    # Menggunakan method terbaru dari google-genai SDK
    response = client.models.embed_content(
        model="gemini-embedding-2",
        contents=teks_uji
    )
    latency_api = time.time() - start_time_api
    
    # Memastikan hasil embedding didapatkan
    # response.embeddings[0].values berisi list angka vektornya
    panjang_dimensi = len(response.embeddings[0].values)
    print(f"✅ Latency API-Based (Gemini API)      : {latency_api:.4f} detik (Dimensi: {panjang_dimensi})")
    
except Exception as e:
    print(f"❌ Gagal memanggil Gemini API: {e}")

print("\nKesimpulan: Waktu pada API sangat bergantung pada kecepatan internet dan server Google, sedangkan Open Source bergantung pada spek CPU/GPU komputer lokal yang digunakan.")