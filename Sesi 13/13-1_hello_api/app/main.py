"""
13.1 FastAPI Fundamentals: endpoint pertama.

Jalankan dari folder 13-1_hello_api/, bukan dari dalam app/:

    uvicorn app.main:app --reload

Lalu buka http://localhost:8000 dan http://localhost:8000/docs.
"""

# TODO 1: import FastAPI dari fastapi, lalu buat objek app = FastAPI()
from fastapi import FastAPI

app = FastAPI()

# TODO 2: tulis endpoint GET "/" dengan fungsi bernama hello()
#         yang mengembalikan {"pesan": "Hello, AI Engineer!"}

@app.get("/")
def hello():
    return {"pesan": "Hello AI Engineer! semuanya? Apa kabar?"}