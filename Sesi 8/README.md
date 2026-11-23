# Demo semantic search

Versi Python ini memecah dua notebook menjadi beberapa langkah kecil agar mudah
dipakai saat mentoring. Jalankan semua perintah dari folder ini.

## Persiapan

```bash
../venv/bin/pip install -r requirements.txt
```

Buat file `.env` di folder ini dan isi:

```text
GEMINI_API_KEY=isi_api_key_di_sini
```

Dataset yang dipakai adalah `faq_dataset/faq_lindungiku.csv`, yang dibaca
menggunakan pandas.

## Urutan demo sesuai ToR

```bash
../venv/bin/python scripts/01_keyword_search.py
../venv/bin/python scripts/02_semantic_search.py
../venv/bin/python scripts/03_ranking_and_distance.py
../venv/bin/python scripts/05_faiss_index.py
../venv/bin/python scripts/06_faiss_query.py
../venv/bin/python scripts/07_faiss_metadata_filter.py
```

File `02_semantic_search.py` membuat `embeddings_faq_csv.npy`. File ini dipakai
ulang oleh langkah-langkah berikutnya supaya API tidak dipanggil berulang kali.
File `05_faiss_index.py` membuat `faq_csv.index`, yang dibaca oleh
`06_faiss_query.py`.

Pemetaan ke kurikulum:

- `01`–`02` adalah 8.1: keyword search dibandingkan dengan semantic search.
- `03` adalah 8.2: ranking berdasarkan similarity score dan perbandingan Euclidean.
- Konsep 8.3 (ANN, HNSW, metadata, dan arsitektur) dibahas oleh mentor tanpa script tambahan.
- `05`–`07` adalah 8.4: indexing, query, menampilkan hasil, dan filter kategori dengan FAISS.
