# Sesi 10 - System & Structured Output

**Model:** gpt-oss:20b

**Tanggal Eksekusi:** 15-11-2026 13:02:46

---

## Data Ulasan Pelanggan

> Barang sampai lumayan cepat, packaging rapi. Tapi pas dibuka, warna bajunya beda sama di foto produk. Katanya navy tapi ini malah kaya hitam kusam.

---

## Demo 1 - System Instruction Separation

**System Instruction:** 


Kamu adalah AI Analyst profesional untuk Toko Online.
Tugasmu adalah menganalisis ulasan pelanggan secara objektif dan ringkas.
Jangan pernah berasumsi di luar informasi yang diberikan pelanggan.


**User Prompt:**

Analisis ulasan berikut: 'Barang sampai lumayan cepat, packaging rapi. Tapi pas dibuka, warna bajunya beda sama di foto produk. Katanya navy tapi ini malah kaya hitam kusam.'

**Hasil Model:**

**Analisis Ulasan Pelanggan**

- **Poin Positif**  
  - Pengiriman cepat.  
  - Packaging rapi dan terjaga.

- **Poin Negatif**  
  - Warna produk tidak sesuai dengan foto: dijanjikan navy, namun tampil lebih gelap/kuning kusam.  
  - Perbedaan warna dapat memengaruhi kepuasan pelanggan dan kepercayaan terhadap deskripsi produk.

**Kesimpulan**  
Ulasan menyoroti keunggulan logistik (kecepatan & kemasan) namun menegaskan ketidaksesuaian warna produk, yang perlu diperbaiki pada deskripsi atau kontrol kualitas.

## Demo 2 - Hyperparameter Tuning

**Temperature:** 0.0

**Top P:** 0.8

**Hasil Model:**

kualitas produk

## Demo 3 - Native JSON Mode

**Raw JSON Output:**

```json
{
    "kategori": "kualitas produk",
    "sentimen": "negatif",
    "alasan_singkat": "warna bajunya berbeda dari foto, seharusnya navy tapi hitam kusam"
}
```

**Parsed Dictionary:**

- **Kategori:** kualitas produk
- **Sentimen:** negatif
- **Alasan:** warna bajunya berbeda dari foto, seharusnya navy tapi hitam kusam

## Demo 4 - Strict Schema Enforcement (Pydantic)

**Pydantic Object:**

- **Tipe Data:** `UlasanAnalysis`
- **Kategori:** ulasan pelanggan
- **Sentimen:** campuran (positif‑negatif)
- **Skor Kecewaan:** 3/5
- **Keluhan Utama:** kualitas produk (warna)

**Structured JSON Output:**

```json
{
    "kategori": "ulasan pelanggan",
    "sentimen": "campuran (positif‑negatif)",
    "skor_kecewaan": 3,
    "keluhan_utama": "kualitas produk (warna)"
}
```



---

*Generated automatically using Ollama and Python.*
