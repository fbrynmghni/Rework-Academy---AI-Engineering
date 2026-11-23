"""
AI logic layer: workflow router dari Sesi 12.4, dipindahkan dari notebook ke modul.

Isinya sama dengan graf pertama di notebook `workflow_router` Sesi 12:
deteksi intent, tiga cabang (rag, alat, langsung), lalu satu node `jawab`.
Nama fungsi dan node sengaja dibiarkan sama dengan Sesi 12, supaya jelas bahwa
ini workflow yang sama, bukan tulisan ulang.

Perubahan dari notebook:
  * tempatnya: dari sel notebook ke file .py, supaya bisa di-import;
  * retrieval diambil dari data layer: `from data.rag_sesi11 import cari`;
  * dua pengaman kecil: jawaban intent yang kosong tidak lagi membuat error,
    dan `jawab` memakai state.get("konteks").

File ini TIDAK diketik ulang saat kelas. API layer tidak memanggilnya langsung;
ia dipanggil lewat app/ai/adapter.py.

Prasyarat:
    sesi-13/.env                 berisi GEMINI_API_KEY
    data/index_lindungiku.faiss  dari Sesi 11
    data/potongan.json           dari Sesi 11
"""

import os

from typing_extensions import TypedDict

from dotenv import load_dotenv
from google import genai
from google.genai import types
from langgraph.graph import StateGraph, START, END

from data.rag_sesi11 import cari

load_dotenv()
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

MODEL = "gemini-2.5-flash"


class State(TypedDict):
    input: str
    intent: str
    konteks: str
    jawaban: str


PROMPT_INTENT = """Klasifikasikan pertanyaan pengguna ke SATU label berikut:

data     - menanyakan isi dokumen kebijakan asuransi LindungiKu
tool     - meminta perhitungan angka, konversi, persentase, atau cicilan
langsung - obrolan umum yang tidak butuh dokumen maupun hitungan

Jawab dengan satu kata saja, tanpa penjelasan.

PERTANYAAN: {input}"""

SAH = {"data", "tool", "langsung"}


def deteksi_intent(state: State) -> dict:
    resp = client.models.generate_content(
        model=MODEL,
        contents=PROMPT_INTENT.format(input=state["input"]),
    )
    kata = (resp.text or "").strip().lower().split()
    label = kata[0].strip(".,:") if kata else ""
    if label not in SAH:
        label = "langsung"          # jaring pengaman
    return {"intent": label}


def kalkulator(a: float, b: float, operator: str) -> str:
    """Hitung operasi aritmatika dua angka.

    Args:
        a: angka pertama
        b: angka kedua
        operator: salah satu dari "+", "-", "*", "/"
    """
    if operator == "/" and b == 0:
        return "tidak terdefinisi, pembagi nol"
    hasil = {"+": a + b, "-": a - b, "*": a * b,
             "/": a / b if b else 0.0}[operator]
    return str(hasil)


def rag(state: State) -> dict:
    potongan = cari(state["input"], k=3)
    return {"konteks": "\n\n".join(p["teks"] for p in potongan)}


def alat(state: State) -> dict:
    resp = client.models.generate_content(
        model=MODEL,
        contents=state["input"],
        config=types.GenerateContentConfig(tools=[kalkulator]),
    )
    return {"konteks": (resp.text or "").strip()}


def langsung(state: State) -> dict:
    return {"konteks": ""}


PROMPT_JAWAB = """Anda adalah asisten layanan nasabah asuransi LindungiKu.
Jawab dengan ramah, ringkas, dan dalam Bahasa Indonesia.

Apabila KONTEKS di bawah terisi, gunakan hanya isi KONTEKS dan jangan menambah
informasi dari luar. Apabila KONTEKS kosong, jawab dari pengetahuan umum saja
dan jangan mengarang isi kebijakan.

KONTEKS:
{konteks}

PERTANYAAN: {input}"""


def jawab(state: State) -> dict:
    resp = client.models.generate_content(
        model=MODEL,
        contents=PROMPT_JAWAB.format(
            konteks=state.get("konteks") or "(kosong)",
            input=state["input"],
        ),
    )
    return {"jawaban": (resp.text or "").strip()}


def pilih_cabang(state: State) -> str:
    return state["intent"]


b = StateGraph(State)

b.add_node("deteksi_intent", deteksi_intent)
b.add_node("rag", rag)
b.add_node("alat", alat)
b.add_node("langsung", langsung)
b.add_node("jawab", jawab)

b.add_edge(START, "deteksi_intent")
b.add_conditional_edges("deteksi_intent", pilih_cabang, {
    "data": "rag",
    "tool": "alat",
    "langsung": "langsung",
})
b.add_edge("rag", "jawab")
b.add_edge("alat", "jawab")
b.add_edge("langsung", "jawab")
b.add_edge("jawab", END)

asisten = b.compile()
