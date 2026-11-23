
import os
import json
from datetime import datetime
from pathlib import Path
import time

from pydantic import BaseModel, Field
import ollama


# ==========================================
# 1. INITIALIZATION
# ==========================================

client = ollama.Client()
MODEL_ID = "gpt-oss:20b"

ulasan_pelanggan = (
    "Barang sampai lumayan cepat, packaging rapi. "
    "Tapi pas dibuka, warna bajunya beda sama di foto produk. "
    "Katanya navy tapi ini malah kaya hitam kusam."
)

# Tempat menampung hasil setiap demo
markdown_sections = []


def add_section(title, content):
    """Menambahkan hasil demo ke dalam Markdown."""
    markdown_sections.append(f"## {title}\n\n{content}\n")


# ==========================================
# 2. BENCHMARK CONFIGURATION
# ==========================================

benchmark_results = []

def timed_chat(demo_name, **kwargs):
    """
    Menjalankan Ollama dan mencatat waktu eksekusi
    serta performa token generation.
    """

    start_time = time.perf_counter()

    response = client.chat(**kwargs)

    end_time = time.perf_counter()

    # Wall-clock duration dalam detik
    wall_time = end_time - start_time

    # Ollama internal metrics (nanoseconds)
    total_duration = getattr(response, "total_duration", None)
    load_duration = getattr(response, "load_duration", None)
    prompt_eval_duration = getattr(
        response, "prompt_eval_duration", None
    )
    eval_duration = getattr(response, "eval_duration", None)

    # Token counts
    prompt_tokens = getattr(response, "prompt_eval_count", None)
    generated_tokens = getattr(response, "eval_count", None)

    # Convert nanoseconds to seconds
    def to_seconds(value):
        return value / 1_000_000_000 if value is not None else None

    # Calculate generation speed
    tokens_per_second = None

    if eval_duration and generated_tokens is not None:
        tokens_per_second = (
            generated_tokens / (eval_duration / 1_000_000_000)
        )

    result = {
        "demo": demo_name,
        "wall_time": wall_time,
        "total_duration": to_seconds(total_duration),
        "load_duration": to_seconds(load_duration),
        "prompt_eval_duration": to_seconds(prompt_eval_duration),
        "eval_duration": to_seconds(eval_duration),
        "prompt_tokens": prompt_tokens,
        "generated_tokens": generated_tokens,
        "tokens_per_second": tokens_per_second
    }

    benchmark_results.append(result)

    return response



# ==========================================
# 3. DEMO 1: SYSTEM INSTRUCTION
# ==========================================

print("--- DEMO 1: System Instruction Separation ---")

system_instruction = """
Kamu adalah AI Analyst profesional untuk Toko Online.
Tugasmu adalah menganalisis ulasan pelanggan secara objektif dan ringkas.
Jangan pernah berasumsi di luar informasi yang diberikan pelanggan.
"""

prompt_user = f"Analisis ulasan berikut: '{ulasan_pelanggan}'"

messages_1 = [
    {"role": "system", "content": system_instruction},
    {"role": "user", "content": prompt_user}
]

response_1 = timed_chat(
    "Demo 1 - System Instruction",
    model=MODEL_ID,
    messages=messages_1,
    options={"temperature": 0.0}
)

hasil_1 = response_1.message.content.strip()

print("[HASIL MODEL]:")
print(hasil_1)

add_section(
    "Demo 1 - System Instruction Separation",
    f"""**System Instruction:** 

{system_instruction}

**User Prompt:**

{prompt_user}

**Hasil Model:**

{hasil_1}
"""
)


# ==========================================
# 4. DEMO 2: HYPERPARAMETER TUNING
# ==========================================

print("\n--- DEMO 2: Hyperparameter Tuning ---")

system_instruction_2 = """
Klasifikasikan ulasan pelanggan ke dalam SATU kata kategori:
pengiriman, kualitas produk, pelayanan, atau harga.
"""

messages_2 = [
    {"role": "system", "content": system_instruction_2},
    {"role": "user", "content": f"Ulasan: '{ulasan_pelanggan}'"}
]

response_2 = timed_chat(
    "Demo 2 - Hyperparameter Tuning",
    model=MODEL_ID,
    messages=messages_2,
    options={
        "temperature": 0.0,
        "top_p": 0.8
    }
)

hasil_2 = response_2.message.content.strip()

print("[HASIL MODEL]:")
print(hasil_2)

add_section(
    "Demo 2 - Hyperparameter Tuning",
    f"""**Temperature:** 0.0

**Top P:** 0.8

**Hasil Model:**

{hasil_2}
"""
)


# ==========================================
# 5. DEMO 3: NATIVE JSON MODE
# ==========================================

print("\n--- DEMO 3: Native JSON Mode ---")

system_instruction_3 = """
Ekstrak ulasan pelanggan ke dalam format JSON.
Gunakan tiga key berikut:
- kategori
- sentimen
- alasan_singkat

Kategori: pengiriman, kualitas produk, pelayanan, harga.
Sentimen: positif, negatif, netral.

Pastikan output berupa JSON valid.
"""

prompt_json = f"Analisis ulasan berikut: '{ulasan_pelanggan}'"

messages_3 = [
    {"role": "system", "content": system_instruction_3},
    {"role": "user", "content": prompt_json}
]

response_3 = timed_chat(
    "Demo 3 - Native JSON Mode",
    model=MODEL_ID,
    messages=messages_3,
    format="json",
    options={"temperature": 0.0}
)

json_text = response_3.message.content.strip()
data_dict = json.loads(json_text)

print("[RAW JSON STRING]:")
print(json_text)

print("\n[PARSED DICTIONARY]:")
print(data_dict)

hasil_3 = f"""**Raw JSON Output:**

```json
{json.dumps(data_dict, indent=4, ensure_ascii=False)}
```

**Parsed Dictionary:**

- **Kategori:** {data_dict.get('kategori')}
- **Sentimen:** {data_dict.get('sentimen')}
- **Alasan:** {data_dict.get('alasan_singkat')}
"""

add_section("Demo 3 - Native JSON Mode", hasil_3)


# ==========================================
# 6. DEMO 4: PYDANTIC STRUCTURED OUTPUT
# ==========================================

print("\n--- DEMO 4: Strict Schema Enforcement ---")


class UlasanAnalysis(BaseModel):

    kategori: str = Field(
        description="Kategori ulasan: pengiriman, kualitas produk, pelayanan, atau harga"
    )

    sentimen: str = Field(
        description="Sentimen ulasan: positif, negatif, atau netral"
    )

    skor_kecewaan: int = Field(
        ge=1,
        le=5,
        description=(
            "Skor kekecewaan: "
            "1=sangat puas, "
            "2=puas, "
            "3=netral, "
            "4=kecewa, "
            "5=sangat kecewa"
        )
    )

    keluhan_utama: str = Field(
        description="Ringkasan satu kalimat keluhan utama pelanggan"
    )


system_instruction_4 = """
Kamu adalah AI Analyst profesional untuk Toko Online.

Tugas:
Analisis ulasan pelanggan secara objektif.

ATURAN KLASIFIKASI:

1. Kategori:
   Pilih tepat satu:
   - pengiriman
   - kualitas produk
   - pelayanan
   - harga

2. Sentimen:
   Pilih tepat satu:
   - positif
   - negatif
   - netral

3. Jika ulasan mengandung pengalaman positif dan negatif:
   Tentukan sentimen berdasarkan keluhan atau pengalaman
   yang paling dominan.

4. Skor kekecewaan:
   - 1 = sangat puas
   - 2 = puas
   - 3 = netral
   - 4 = kecewa
   - 5 = sangat kecewa

5. Jangan memberikan skor 0 atau lebih dari 5.

6. Jangan mengarang informasi di luar ulasan pelanggan.

Berikan hasil sesuai structured output schema.
"""

messages_4 = [
    {
        "role": "system",
        "content": "Kamu adalah sistem otomatis pemrosesan ulasan pelanggan."
    },
    {
        "role": "user",
        "content": f"Analisis ulasan berikut: '{ulasan_pelanggan}'"
    }
]

response_4 = timed_chat(
    "Demo 4 - Strict Schema Enforcement (Pydantic)",
    model=MODEL_ID,
    messages=messages_4,
    format=UlasanAnalysis.model_json_schema(),
    options={"temperature": 0.0}
)

# Validasi JSON menggunakan Pydantic
has_parsed = UlasanAnalysis.model_validate_json(
    response_4.message.content
)

print("[PYDANTIC OBJECT]:")
print(f"Tipe Data       : {type(has_parsed)}")
print(f"Kategori        : {has_parsed.kategori}")
print(f"Sentimen        : {has_parsed.sentimen}")
print(f"Skor Kecewaan   : {has_parsed.skor_kecewaan}/5")
print(f"Keluhan Utama   : {has_parsed.keluhan_utama}")


hasil_4 = f"""**Pydantic Object:**

- **Tipe Data:** `{type(has_parsed).__name__}`
- **Kategori:** {has_parsed.kategori}
- **Sentimen:** {has_parsed.sentimen}
- **Skor Kecewaan:** {has_parsed.skor_kecewaan}/5
- **Keluhan Utama:** {has_parsed.keluhan_utama}

**Structured JSON Output:**

```json
{has_parsed.model_dump_json(indent=4)}
```
"""

add_section("Demo 4 - Strict Schema Enforcement (Pydantic)", hasil_4)


# ==========================================
# 7. EXPORT TO MARKDOWN
# ==========================================

print("\n--- EXPORTING MARKDOWN ---")

# Membuat folder output jika belum tersedia
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Nama file Markdown
OUTPUT_FILE = OUTPUT_DIR / "system_and_structured_output.md"

# Menyusun seluruh hasil demo
markdown_content = f"""# Sesi 10 - System & Structured Output

**Model:** {MODEL_ID}

**Tanggal Eksekusi:** {datetime.now().strftime("%d-%m-%Y %H:%M:%S")}

---

## Data Ulasan Pelanggan

> {ulasan_pelanggan}

---

{"".join(markdown_sections)}

---

*Generated automatically using Ollama and Python.*
"""

# Menulis hasil ke file Markdown
OUTPUT_FILE.write_text(
    markdown_content,
    encoding="utf-8"
)

print(f"Markdown berhasil disimpan!")
print(f"Lokasi file: {OUTPUT_FILE.resolve()}")


# ==========================================
# 8. EXPORT BENCHMARK REPORT
# ==========================================

print("\n--- EXPORTING BENCHMARK REPORT ---")

def format_metric(value, suffix="s"):
    if value is None:
        return "N/A"
    return f"{value:.3f} {suffix}"


# Membuat tabel benchmark
benchmark_table = """
| Demo | Wall Time | Ollama Total | Load Time | Prompt Eval | Generation | Tokens | Tokens/sec |
|---|---:|---:|---:|---:|---:|---:|---:|
"""

for result in benchmark_results:

    benchmark_table += (
        f"| {result['demo']} "
        f"| {format_metric(result['wall_time'])} "
        f"| {format_metric(result['total_duration'])} "
        f"| {format_metric(result['load_duration'])} "
        f"| {format_metric(result['prompt_eval_duration'])} "
        f"| {format_metric(result['eval_duration'])} "
        f"| {result['generated_tokens'] if result['generated_tokens'] is not None else 'N/A'} "
        f"| {format_metric(result['tokens_per_second'], 'tok/s')} |\n"
    )


# Menghitung total waktu
total_wall_time = sum(
    item["wall_time"] for item in benchmark_results
)

# Total internal duration Ollama
available_total = [
    item["total_duration"]
    for item in benchmark_results
    if item["total_duration"] is not None
]

total_model_time = (
    sum(available_total) if available_total else None
)

total_generated_tokens = sum(
    item["generated_tokens"] or 0
    for item in benchmark_results
)

# Membuat laporan Markdown
benchmark_content = f"""# Ollama Model Performance Benchmark

## Model Information

- **Model:** {MODEL_ID}
- **Runtime:** Ollama Python SDK
- **Date:** {datetime.now().strftime("%d-%m-%Y %H:%M:%S")}
- **Total Demos:** {len(benchmark_results)}

---

## 1. Execution Performance

{benchmark_table}

---

## 2. Performance Summary

| Metric | Result |
|---|---:|
| Total Python Wall Time (API calls) | {format_metric(total_wall_time)} |
| Total Ollama Duration | {format_metric(total_model_time)} |
| Total Generated Tokens | {total_generated_tokens} |
| Number of Model Requests | {len(benchmark_results)} |

---

## 3. Metric Explanation

- **Wall Time:** Actual elapsed time measured by Python.
- **Ollama Total:** Total processing duration reported by Ollama.
- **Load Time:** Time required to load the model.
- **Prompt Eval:** Time required to process input tokens.
- **Generation:** Time required to generate output tokens.
- **Tokens:** Number of generated tokens.
- **Tokens/sec:** Model generation speed.

---

## 4. Benchmark Notes

1. All demos use model `{MODEL_ID}`.
2. Model parameters may affect generation speed.
3. First execution may include model loading time.
4. Performance can vary depending on system resources,
   available RAM, and concurrent processes.
5. Wall Time and Ollama Total Duration are different
   measurements and should not be added together.

---

*Generated automatically using Python and Ollama.*
"""

# Simpan benchmark report
BENCHMARK_FILE = OUTPUT_DIR / "ollama_benchmark.md"

BENCHMARK_FILE.write_text(
    benchmark_content,
    encoding="utf-8"
)

print("Benchmark berhasil disimpan!")
print(f"Lokasi file: {BENCHMARK_FILE.resolve()}")

print(f"\nTotal Wall Time : {total_wall_time:.3f} seconds")

if total_model_time is not None:
    print(f"Total Model Time: {total_model_time:.3f} seconds")

