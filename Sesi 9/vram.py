# ==============================================================================
# REWORK ACADEMY - LIVE BOOTCAMP
# Sesi 9.4: Model Selection Strategy & Guided Practical
# Task: Text Summarization Bahasa Indonesia
# ==============================================================================

# Langkah 0: Install library yang dibutuhkan (jika belum terinstall)
# !pip install -q transformers torch sentencepiece

import torch
from transformers import pipeline, AutoTokenizer, EncoderDecoderModel

# ------------------------------------------------------------------------------
# BAGIAN 1: GUIDED PRACTICAL - RUNNING SUMMARIZATION MODEL
# ------------------------------------------------------------------------------

print("="*70)
print("1. MEMUAT MODEL SUMMARIZATION")
print("="*70)

MODEL_NAME = "cahya/bert2bert-indonesian-summarization"

try:
    # Memuat pipeline summarization Hugging Face
    # Pipeline mengurusi tokenization, model forward pass, dan decoding secara otomatis
    summarizer = pipeline(
        task="summarization",
        model=MODEL_NAME,
        tokenizer=MODEL_NAME
    )
    print(f"✓ Berhasil memuat model: {MODEL_NAME}\n")
except Exception as e:
    print(f"Gagal memuat pipeline: {e}")
    # Fallback manual jika pipeline mengalami kendala dengan arsitektur EncoderDecoder
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = EncoderDecoderModel.from_pretrained(MODEL_NAME)
    summarizer = None


# Contoh artikel berita Bahasa Indonesia (panjang)
artikel_indonesia = """
Kementerian Komunikasi dan Informatika (Kominfo) terus mengakselerasi program digitalisasi nasional 
guna memperkuat infrastruktur teknologi informasi di seluruh wilayah Indonesia, termasuk daerah 3T 
(Tertinggal, Terdepan, dan Terluar). Program ini bertujuan untuk memangkas kesenjangan digital dan 
memastikan bahwa seluruh lapisan masyarakat mendapatkan akses internet yang layak dan berkualitas tinggi. 

Menteri Kominfo menyatakan bahwa konektivitas internet yang merata merupakan fondasi utama bagi 
pertumbuhan ekonomi digital. Dengan berkembangnya akses internet, para pelaku Usaha Mikro, Kecil, dan 
Menengah (UMKM) dapat memperluas jangkauan pasar mereka hingga ke tingkat nasional maupun internasional. 

Selain pembangunan infrastruktur fisik seperti jaringan fiber optik dan menara BTS, pemerintah juga 
fokus pada peningkatan literasi digital masyarakat. Program pelatihan digital talent scholarship terus 
digelar untuk membekali generasi muda dengan keterampilan di bidang AI, cybersecurity, cloud computing, 
serta AI Engineering agar mampu bersaing di era industri 4.0.
"""

print("Teks Asli (Panjang Karakter:", len(artikel_indonesia), "):")
print("-" * 50)
print(artikel_indonesia.strip())
print("-" * 50)


# Jalankan Inference Summarization
print("\n[Sedang Menjalankan Peringkasan Teks...]")

if summarizer:
    res = summarizer(
        artikel_indonesia, 
        max_length=80, 
        min_length=20, 
        do_sample=False
    )
    hasil_ringkasan = res[0]['summary_text']
else:
    # Manual inference jika menggunakan model/tokenizer objek langsung
    inputs = tokenizer(artikel_indonesia, return_tensors="pt", max_length=512, truncation=True)
    summary_ids = model.generate(inputs["input_ids"], max_length=80, min_length=20, num_beams=4)
    hasil_ringkasan = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

print("\nHasil Ringkasan (Summarization Output):")
print("=" * 50)
print(hasil_ringkasan)
print("=" * 50)


# ------------------------------------------------------------------------------
# BAGIAN 2: ESTIMASI HARDWARE REQUIREMENT (VRAM CALCULATION)
# ------------------------------------------------------------------------------
# Note: Kalkulasi dilakukan secara matematis/konseptual berdasarkan parameter
# tanpa harus benar-benar memuat model besar ke GPU local.

print("\n" + "="*70)
print("2. ESTIMASI KEBUTUHAN HARDWARE / VRAM (KONSEP SELEKSI MODEL)")
print("="*70)

def calculate_vram_requirement(num_params_b, precision="fp16", overhead_factor=1.25):
    """
    Menghitung estimasi kebutuhan VRAM (GB) untuk Inference Model.
    
    Parameters:
    - num_params_b: Jumlah parameter dalam Miliar (Billion / B)
    - precision: FP32 (4 bytes), FP16/BF16 (2 bytes), INT8 (1 byte), INT4 (0.5 byte)
    - overhead_factor: Estimasi buffer untuk activation memory & PyTorch CUDA context (~25%)
    """
    bytes_per_param = {
        "fp32": 4,
        "fp16": 2,
        "bf16": 2,
        "int8": 1,
        "int4": 0.5
    }
    
    bytes_val = bytes_per_param.get(precision.lower(), 2)
    # Total Byte Model = Parameter Count (in Billion) * 1e9 * Bytes per Param
    model_size_gb = (num_params_b * 1e9 * bytes_val) / (1024**3)
    total_vram_gb = model_size_gb * overhead_factor
    return model_size_gb, total_vram_gb

# Daftar model pembanding untuk demonstrasi peserta
candidate_models = [
    {"name": "(Model Praktik)", "params_b": 0.3},
    {"name": "IndoT5-Base / Llama-3.2-1B", "params_b": 1.0},
    {"name": "Llama-3.1-8B / Mistral-7B", "params_b": 8.0},
    {"name": "Llama-3.3-70B", "params_b": 70.0}
]

print(f"{'Nama Model':<40} | {'FP16 Base (GB)':<15} | {'Est. Total VRAM (GB)':<20}")
print("-" * 80)

for m in candidate_models:
    base_gb, total_vram = calculate_vram_requirement(m["params_b"], precision="fp16")
    print(f"{m['name']:<40} | {base_gb:<15.2f} | {total_vram:<20.2f}")

print("-" * 80)
print("*Catatan: Est. Total VRAM sudah memperhitungkan overhead PyTorch/CUDA (~25%).")


# ------------------------------------------------------------------------------
# BAGIAN 3: RINGKASAN KERANGKA PENGAMBILAN KEPUTUSAN (AI ENGINEER CHEATSHEET)
# ------------------------------------------------------------------------------

print("\n" + "="*70)
print("3. KERANGKA STRATEGI PEMILIHAN MODEL (MODEL SELECTION MATRIX)")
print("="*70)

decision_matrix = """
+-----------------------+------------------------+---------------------------------------+
| Kriteria              | Open-Source (Small/Mid)| Proprietary API (e.g. Gemini / OpenAI)|
+-----------------------+------------------------+---------------------------------------+
| Contoh Model          | bert2gpt-indosum (0.3B)| Gemini 1.5 Flash / GPT-4o-mini        |
| Latency               | Sangat Rendah (<200ms) | Sedang (Tergantung Koneksi & Queue)   |
| Hardware Requirement  | Butuh GPU Murah / CPU  | Nol (Managed Infrastructure)          |
| Privasi Data          | 100% Kontrol Internal  | Data terkirim via API                 |
| Biaya Jangka Panjang  | Tetap (Fixed GPU Cost) | Pay-as-you-go (Variabel per Token)    |
| Kualitas Summarization| Baik untuk task spesifik| Sangat Tinggi untuk konteks kompleks  |
+-----------------------+------------------------+---------------------------------------+
"""
print(decision_matrix)

# W1105 13:29:41.791000 5066 torch/distributed/elastic/multiprocessing/redirects.py:35] NOTE: Redirects are currently not supported in MacOs.
# ======================================================================
# 1. MEMUAT MODEL SUMMARIZATION
# ======================================================================
# Gagal memuat pipeline: 'The task summarization has been removed from transformers. Use the `text-generation` pipeline with a chat model instead. See the migration guide for more details: https://github.com/huggingface/transformers/blob/main/MIGRATION_GUIDE_V5.md#pipelines'
# Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.
# Loading weights: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 523/523 [00:00<00:00, 52482.74it/s]
# Teks Asli (Panjang Karakter: 1089 ):
# --------------------------------------------------
# Kementerian Komunikasi dan Informatika (Kominfo) terus mengakselerasi program digitalisasi nasional 
# guna memperkuat infrastruktur teknologi informasi di seluruh wilayah Indonesia, termasuk daerah 3T 
# (Tertinggal, Terdepan, dan Terluar). Program ini bertujuan untuk memangkas kesenjangan digital dan 
# memastikan bahwa seluruh lapisan masyarakat mendapatkan akses internet yang layak dan berkualitas tinggi. 

# Menteri Kominfo menyatakan bahwa konektivitas internet yang merata merupakan fondasi utama bagi 
# pertumbuhan ekonomi digital. Dengan berkembangnya akses internet, para pelaku Usaha Mikro, Kecil, dan 
# Menengah (UMKM) dapat memperluas jangkauan pasar mereka hingga ke tingkat nasional maupun internasional. 

# Selain pembangunan infrastruktur fisik seperti jaringan fiber optik dan menara BTS, pemerintah juga 
# fokus pada peningkatan literasi digital masyarakat. Program pelatihan digital talent scholarship terus 
# digelar untuk membekali generasi muda dengan keterampilan di bidang AI, cybersecurity, cloud computing, 
# serta AI Engineering agar mampu bersaing di era industri 4.0.
# --------------------------------------------------

# [Sedang Menjalankan Peringkasan Teks...]

# Hasil Ringkasan (Summarization Output):
# ==================================================
# pemerintah terus mengakselerasi program digitalisasi nasional guna memperkuat infrastruktur teknologi informasi di seluruh wilayah indonesia, termasuk daerah 3t.
# ==================================================

# ======================================================================
# 2. ESTIMASI KEBUTUHAN HARDWARE / VRAM (KONSEP SELEKSI MODEL)
# ======================================================================
# Nama Model                               | FP16 Base (GB)  | Est. Total VRAM (GB)
# --------------------------------------------------------------------------------
# (Model Praktik)                          | 0.56            | 0.70                
# IndoT5-Base / Llama-3.2-1B               | 1.86            | 2.33                
# Llama-3.1-8B / Mistral-7B                | 14.90           | 18.63               
# Llama-3.3-70B                            | 130.39          | 162.98              
# --------------------------------------------------------------------------------
# *Catatan: Est. Total VRAM sudah memperhitungkan overhead PyTorch/CUDA (~25%).

# ======================================================================
# 3. KERANGKA STRATEGI PEMILIHAN MODEL (MODEL SELECTION MATRIX)
# ======================================================================

# +-----------------------+------------------------+---------------------------------------+
# | Kriteria              | Open-Source (Small/Mid)| Proprietary API (e.g. Gemini / OpenAI)|
# +-----------------------+------------------------+---------------------------------------+
# | Contoh Model          | bert2gpt-indosum (0.3B)| Gemini 1.5 Flash / GPT-4o-mini        |
# | Latency               | Sangat Rendah (<200ms) | Sedang (Tergantung Koneksi & Queue)   |
# | Hardware Requirement  | Butuh GPU Murah / CPU  | Nol (Managed Infrastructure)          |
# | Privasi Data          | 100% Kontrol Internal  | Data terkirim via API                 |
# | Biaya Jangka Panjang  | Tetap (Fixed GPU Cost) | Pay-as-you-go (Variabel per Token)    |
# | Kualitas Summarization| Baik untuk task spesifik| Sangat Tinggi untuk konteks kompleks  |
# +-----------------------+------------------------+---------------------------------------+