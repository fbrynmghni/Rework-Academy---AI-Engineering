# data/ : data layer

Folder ini adalah data layer: tempat knowledge base dari Sesi 11 disimpan dan diambil.

Dua file dari folder Sesi 11 atau Sesi 12 Anda tinggal di sini:

- `index_lindungiku.faiss`
- `potongan.json`

Keduanya harus berasal dari proses ingestion yang sama. Salin keduanya ke `data/` milik `13-2_arsitektur` dan `13-4_layanan_ai`. Folder `data/` di `13-3_validasi` boleh dibiarkan tanpa index, karena 13.3 belum memakai AI layer.

`rag_sesi11.py` adalah kode retrieval-nya. Hanya AI logic layer (`app/ai/workflow_sesi12.py`) yang memakainya. API layer (`app/main.py`) tidak pernah menyentuh folder ini.

Uji data layer sendirian, dari folder bagian (satu tingkat di atas folder ini):

```
python -m data.rag_sesi11
```
