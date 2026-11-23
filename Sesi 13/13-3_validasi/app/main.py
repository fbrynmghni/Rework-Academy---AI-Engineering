"""
API layer: endpoint saja, tanpa logika AI.

13.3 API Endpoint Design: endpoint /pesan dengan request validation.

Jalankan dari folder 13-3_validasi/:

    uvicorn app.main:app --reload
"""

from fastapi import FastAPI
from app.schemas import Pesanan
app = FastAPI()


@app.get("/")
def hello():
    return {"pesan": "Hello, AI Engineer!"}


# TODO 1 (tanpa validation): tulis endpoint POST "/pesan" dengan fungsi
#         create_order(data: dict). Jika data["jumlah"] > 10, kembalikan
#         {"status": "ok", "diskon": True}, selain itu {"status": "ok", "diskon": False}.
#         Di Postman, kirim request "13.3 Validation > POST /pesan - benar", lalu
#         "POST /pesan - jumlah berupa teks". Lihat status code di Postman dan
#         pesan error di terminal.

@app.post("/pesan")
def create_order(data: Pesanan):
    if data.jumlah > 10:
        return {"status": "ok", "diskon": True}
    return {"status": "ok", "diskon": False}


# TODO 2b (dengan validation): setelah TODO 2a di app/schemas.py selesai,
#         tambahkan `from app.schemas import Pesanan` di atas, ganti data: dict
#         menjadi data: Pesanan, dan ganti isi fungsinya menjadi
#         return {"status": "ok", "data": data}
#         Kirim body yang sama. Bandingkan status code-nya.
