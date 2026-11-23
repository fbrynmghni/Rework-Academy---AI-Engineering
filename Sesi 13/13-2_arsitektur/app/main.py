"""
API layer: endpoint saja, tanpa logika AI.

13.2 AI Service Architecture: kode endpoint belum berubah dari 13.1.
Yang baru adalah strukturnya:

    app/main.py   API layer        menerima request, mengirim response
    app/ai/       AI logic layer   workflow Sesi 12 dan prompt
    data/         data layer       index dan retrieval dari Sesi 11

main.py belum memanggil AI layer. Itu terjadi di 13.4, lewat app/ai/adapter.py.

Jalankan dari folder 13-2_arsitektur/:

    uvicorn app.main:app --reload
"""

# TODO (13.2): tidak ada kode baru di bagian ini. Karena setiap layer terpisah,
#   masing-masing bisa diuji sendiri. Dari folder 13-2_arsitektur/, jalankan:
#
#     python -m data.rag_sesi11      menguji data layer saja
#     python -m app.ai.adapter       menguji AI logic layer saja, tanpa server
#     uvicorn app.main:app --reload  menguji API layer, lewat Postman
#
#   Jika data layer menulis "index_lindungiku.faiss tidak ditemukan", salin
#   index dan potongan.json ke folder data/ (lihat data/README.md).

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def hello():
    return {"pesan": "Hello, AI Engineer!"}
