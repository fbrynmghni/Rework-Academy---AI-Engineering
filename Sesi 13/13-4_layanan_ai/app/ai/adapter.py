"""
Adapter: satu-satunya pintu antara API layer dan AI logic layer.

main.py hanya mengenal tiga fungsi dari file ini:

    answer_question(pertanyaan)  -> {"jawaban": ..., "intent": ...}    untuk /ask
    summarize_text(teks)         -> {"ringkasan": ...}                 untuk /summarize
    classify_text(teks)          -> {"label": ...}                     untuk /analyze

Bentuk hasil di atas adalah janji (kontrak) kepada API layer. Isi workflow,
state LangGraph, dan prompt boleh berubah. Selama bentuk hasilnya tetap,
main.py dan client yang memanggil API tidak ikut berubah.

Stub
----
Jika workflow Sesi 12 atau client Gemini gagal dimuat (index Sesi 11 hilang,
library belum terpasang, API key kosong), adapter TIDAK membuat server mati.
Ia memakai pengganti (stub) yang:

  * menunggu STUB_SECONDS detik dengan cara blocking, persis seperti panggilan
    LLM sungguhan, sehingga demo sync vs async tetap terlihat;
  * mengembalikan jawaban palsu yang jelas bertanda [STUB];
  * mencetak peringatan besar di terminal setiap kali dipanggil.

Cara menyambungkan yang asli ada di Troubleshooting - Sesi 13, bagian C.

Uji AI layer sendirian, tanpa server, dari folder 13-4_layanan_ai/:

    python -m app.ai.adapter
"""

import time
import traceback

from app.config import STUB_SECONDS


def _warn_load_failed(bagian):
    print("\n" + "=" * 70)
    print(f"[adapter] PERINGATAN: {bagian} GAGAL dimuat.")
    print("[adapter] Server tetap jalan memakai STUB. Penyebabnya:")
    traceback.print_exc(limit=1)
    print("=" * 70 + "\n")


# ---------------------------------------------------------------------------
# Memuat AI logic layer. SystemExit dari data/rag_sesi11.py juga ditangkap.
# ---------------------------------------------------------------------------

try:
    from app.ai.workflow_sesi12 import asisten
    WORKFLOW_LOADED = True
    print("[adapter] Workflow Sesi 12 berhasil dimuat.")
except (Exception, SystemExit):
    _warn_load_failed("workflow Sesi 12")
    asisten = None
    WORKFLOW_LOADED = False

try:
    from app.ai import text_tasks
    TEXT_TASKS_LOADED = True
except (Exception, SystemExit):
    _warn_load_failed("client Gemini untuk /summarize dan /analyze")
    text_tasks = None
    TEXT_TASKS_LOADED = False


def _stub_wait():
    print("\n" + "!" * 70)
    print("!!  STUB AKTIF: jawaban di bawah BUKAN dari LLM.")
    print("!!  Lihat Troubleshooting - Sesi 13, bagian C.")
    print("!" * 70 + "\n")
    time.sleep(STUB_SECONDS)            # blocking, seperti panggilan LLM asli


# ---------------------------------------------------------------------------
# Tiga fungsi yang boleh dipanggil API layer
# ---------------------------------------------------------------------------

def answer_question(pertanyaan):
    if asisten is None:
        _stub_wait()
        return {"jawaban": f"[STUB] Pertanyaan '{pertanyaan}' diterima. "
                           "Workflow Sesi 12 belum tersambung.",
                "intent": "stub"}
    hasil = asisten.invoke({"input": pertanyaan})
    # Hanya dua field ini yang keluar. Isi state lain (misalnya konteks hasil
    # retrieval) tetap di dalam AI logic layer.
    return {"jawaban": hasil.get("jawaban", ""), "intent": hasil.get("intent", "")}


def summarize_text(teks):
    if text_tasks is None:
        _stub_wait()
        return {"ringkasan": "[STUB] LLM belum tersambung."}
    return text_tasks.summarize_text(teks)


def classify_text(teks):
    if text_tasks is None:
        _stub_wait()
        return {"label": "stub"}
    return text_tasks.classify_text(teks)


if __name__ == "__main__":
    print(answer_question("Berapa lama masa tunggu klaim rawat inap?"))
