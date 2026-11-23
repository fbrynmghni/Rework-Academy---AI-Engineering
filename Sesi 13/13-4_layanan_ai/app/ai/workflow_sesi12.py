
"""
AI logic layer: workflow router dari Sesi 12.4, dipindahkan dari notebook ke modul.

Workflow:
    deteksi_intent
        ├── data      -> rag       -> jawab
        ├── tool      -> alat      -> jawab
        └── langsung  -> langsung -> jawab

Mulai 13.4:
    Model dan client Ollama diambil dari app/config.py.

Prasyarat:
    Ollama aktif dan model tersedia secara lokal.
    data/index_lindungiku.faiss
    data/potongan.json
"""

from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

from app.config import MODEL, create_ollama_client
from data.rag_sesi11 import cari

client = create_ollama_client()


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
    resp = client.chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": PROMPT_INTENT.format(input=state["input"]),
            }
        ],
    )

    teks = (resp.message.content or "").strip().lower()
    kata = teks.split()
    label = kata[0].strip(".,:") if kata else ""

    if label not in SAH:
        label = "langsung"

    return {"intent": label}


def kalkulator(a: float, b: float, operator: str) -> str:
    """Hitung operasi aritmatika dua angka.

    Args:
        a: angka pertama
        b: angka kedua
        operator: salah satu dari "+", "-", "*", "/"
    """
    if operator not in {"+", "-", "*", "/"}:
        return "Operator tidak dikenal."

    if operator == "/" and b == 0:
        return "Tidak terdefinisi, pembagi nol."

    hasil = {
        "+": a + b,
        "-": a - b,
        "*": a * b,
        "/": a / b,
    }[operator]

    return str(hasil)


def rag(state: State) -> dict:
    potongan = cari(state["input"], k=3)

    return {
        "konteks": "\n\n".join(
            p["teks"] for p in potongan
        )
    }


def alat(state: State) -> dict:
    """
    Memanggil kalkulator menggunakan native tool calling Ollama.
    """

    messages = [
        {
            "role": "user",
            "content": (
                "Gunakan tool kalkulator untuk menyelesaikan "
                "permintaan berikut: " + state["input"]
            ),
        }
    ]

    resp = client.chat(
        model=MODEL,
        messages=messages,
        tools=[kalkulator],
    )

    tool_calls = resp.message.tool_calls

    # Jika model tidak menghasilkan tool call,
    # gunakan respons teksnya sebagai fallback.
    if not tool_calls:
        return {
            "konteks": (resp.message.content or "").strip()
        }

    # Simpan pesan assistant yang berisi permintaan tool.
    messages.append(
        {
            "role": "assistant",
            "content": resp.message.content or "",
            "tool_calls": [
                call.model_dump(exclude_none=True)
                for call in tool_calls
            ],
        }
    )

    # Jalankan setiap tool call dari model.
    for call in tool_calls:
        nama_tool = call.function.name
        argumen = call.function.arguments

        if nama_tool == "kalkulator":
            hasil = kalkulator(**argumen)
        else:
            hasil = f"Tool {nama_tool} tidak tersedia."

        messages.append(
            {
                "role": "tool",
                "content": hasil,
            }
        )

    # Kirim hasil tool kembali ke model agar dibuat menjadi jawaban.
    final_resp = client.chat(
        model=MODEL,
        messages=messages,
    )

    return {
        "konteks": (final_resp.message.content or "").strip()
    }


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
    resp = client.chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": PROMPT_JAWAB.format(
                    konteks=state.get("konteks") or "(kosong)",
                    input=state["input"],
                ),
            }
        ],
    )

    return {
        "jawaban": (resp.message.content or "").strip()
    }


def pilih_cabang(state: State) -> str:
    return state["intent"]


b = StateGraph(State)

b.add_node("deteksi_intent", deteksi_intent)
b.add_node("rag", rag)
b.add_node("alat", alat)
b.add_node("langsung", langsung)
b.add_node("jawab", jawab)

b.add_edge(START, "deteksi_intent")

b.add_conditional_edges(
    "deteksi_intent",
    pilih_cabang,
    {
        "data": "rag",
        "tool": "alat",
        "langsung": "langsung",
    },
)

b.add_edge("rag", "jawab")
b.add_edge("alat", "jawab")
b.add_edge("langsung", "jawab")
b.add_edge("jawab", END)

asisten = b.compile()
