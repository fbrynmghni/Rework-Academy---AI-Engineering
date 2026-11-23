"""
API layer: endpoint saja, tanpa logika AI.

13.4 LLM Integration: API yang production-ready.

main.py hanya boleh memanggil tiga fungsi dari app/ai/adapter.py:
    answer_question(pertanyaan)   summarize_text(teks)   classify_text(teks)
Ia tidak perlu tahu bahwa di belakangnya ada LangGraph, RAG, atau prompt.

Jalankan dari folder 13-4_layanan_ai/:

    uvicorn app.main:app --reload
"""

from fastapi import FastAPI

from app.schemas import Pesanan, Pertanyaan, Teks
from app.ai.adapter import answer_question, summarize_text, classify_text
import asyncio

app = FastAPI()


@app.get("/")
def hello():
    return {"pesan": "Hello, AI Engineer!"}


@app.post("/pesan")
def create_order(data: Pesanan):
    return {"status": "ok", "data": data}


# TODO 1b (demo sync): setelah TODO 1a di app/schemas.py selesai, ubah baris
#         import schemas di atas menjadi `from app.schemas import Pesanan, Pertanyaan`
#         dan tambahkan `from app.ai.adapter import answer_question`.
#         Tulis endpoint POST "/ask" sebagai async def ask(data: Pertanyaan) yang
#         memanggil hasil = answer_question(data.pertanyaan) secara langsung, lalu
#         return {"status": "ok", "data": hasil}
#         Kirim dua request hampir bersamaan dari dua tab Postman, catat waktunya.

@app.post("/ask_sync")
def ask_sync(data: Pertanyaan):
    hasil = answer_question(data.pertanyaan)
    return {"status": "ok",
                "hasil": hasil}

# TODO 2 (demo async): tambahkan `import asyncio` di paling atas, lalu ganti
#         panggilannya menjadi
#         hasil = await asyncio.to_thread(answer_question, data.pertanyaan)
#         Kirim dua request bersamaan lagi. Bandingkan waktunya.

@app.post("/ask")
async def ask(data: Pertanyaan):
    hasil = await asyncio.to_thread(answer_question, data.pertanyaan)
    return {"status": "ok",
            "hasil": hasil}

# TODO 3b: setelah TODO 3a di app/schemas.py selesai, tambahkan Teks ke baris
#         `from app.schemas import ...` dan tambahkan summarize_text, classify_text
#         ke baris `from app.ai.adapter import ...`. Lalu tulis endpoint
#         POST "/summarize" (memanggil summarize_text) dan POST "/analyze"
#         (memanggil classify_text), masing-masing dengan data: Teks. Bentuknya
#         sama dengan /ask: await asyncio.to_thread(fungsi, data.teks).

@app.post("/summarize")
async def summarize(data: Teks):
    hasil = await asyncio.to_thread(summarize_text, data.teks)
    return {"status": "ok",
            "hasil": hasil}

@app.post("/analyze")
async def analyze(data: Teks):
    hasil = await asyncio.to_thread(classify_text, data.teks)
    return {"status": "ok",
            "hasil": hasil}

# TODO 4 (error handling): tambahkan `from fastapi.responses import JSONResponse`,
#         lalu buat fungsi:
#
#             def error_response(status_code, pesan, detail=None):
#                 isi = {"status": "error", "pesan": pesan}
#                 if detail is not None:
#                     isi["detail"] = detail
#                 return JSONResponse(status_code=status_code, content=isi)
#
#         Bungkus panggilan di /ask, /summarize, dan /analyze dengan
#             try:
#                 hasil = await asyncio.to_thread(...)
#             except Exception as e:
#                 return error_response(503, f"LLM gagal menjawab: {type(e).__name__}")
#         Pesannya: "menjawab" untuk /ask, "meringkas" untuk /summarize,
#         "menganalisis" untuk /analyze.
#         Uji: tambahkan sementara `raise RuntimeError("uji")` sebagai baris pertama
#         di dalam try pada /ask, kirim satu request, lihat 503 di Postman, lalu
#         hapus baris itu.
#
# TODO 5 (validation 422 yang seragam): ubah baris import FastAPI menjadi
#         `from fastapi import FastAPI, Request`, tambahkan
#         `from fastapi.exceptions import RequestValidationError`, lalu tulis:
#
#             @app.exception_handler(RequestValidationError)
#             async def validation_error_handler(request: Request, exc: RequestValidationError):
#                 detail = [
#                     {
#                         "field": ".".join(str(bagian) for bagian in err["loc"][1:]) or "body",
#                         "masalah": err["msg"],
#                     }
#                     for err in exc.errors()
#                 ]
#                 return error_response(422, "Input tidak sesuai format.", detail)
#
#         err["loc"] berisi misalnya ("body", "jumlah"). Item pertama selalu
#         "body", jadi kita buang. err["msg"] berisi alasannya.
#         Kirim lagi "POST /pesan - jumlah berupa teks" dan bandingkan isinya.
#
# TODO 6: ubah hello() supaya ikut bentuk yang sama:
#         return {"status": "ok", "data": {"pesan": "Hello, AI Engineer!"}}
