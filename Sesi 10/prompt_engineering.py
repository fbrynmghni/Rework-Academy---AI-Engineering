
import json
import time
import re
import ollama

from pathlib import Path
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)


# ==================================================
# 1. SETUP
# ==================================================

client = ollama.Client()

MODEL_ID = "qwen3.8:27b-mlx"
JSON_FILE_PATH = Path("dataset_test.json")

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

REPORT_FILE = OUTPUT_DIR / "qwen_prompt_engineering_report.md"

VALID_CATEGORIES = [
    "pengiriman",
    "kualitas produk",
    "pelayanan",
    "harga"
]

TEMPERATURE = 0.0

# Load dataset
with open(JSON_FILE_PATH, "r", encoding="utf-8") as file:
    test_set = json.load(file)

if not test_set:
    raise ValueError("Dataset kosong.")

for index, item in enumerate(test_set):
    if "ulasan" not in item or "ground_truth" not in item:
        raise ValueError(f"Format data ke-{index + 1} tidak valid.")

    item["ground_truth"] = str(item["ground_truth"]).strip().lower()

    if item["ground_truth"] not in VALID_CATEGORIES:
        raise ValueError(
            f"Ground truth tidak dikenal pada data ke-{index + 1}: "
            f"{item['ground_truth']}"
        )

print("=" * 55)
print("QWEN PROMPT ENGINEERING EXPERIMENT")
print("=" * 55)
print(f"Model       : {MODEL_ID}")
print(f"Dataset     : {JSON_FILE_PATH}")
print(f"Total Data  : {len(test_set)}")
print(f"Temperature : {TEMPERATURE}")


# ==================================================
# 2. DYNAMIC PROMPT TEMPLATE
# ==================================================

def build_prompt(ulasan_text: str, mode: str = "vague") -> str:

    if mode == "vague":

        return f"Klasifikasikan ulasan ini: {ulasan_text}"

    elif mode == "optimized":

        return f"""
[PERSONA]
Kamu adalah Data Classifier profesional di e-commerce.

[TASK]
Klasifikasikan ulasan pelanggan ke dalam SATU kategori utama
dari daftar berikut:

- pengiriman
- kualitas produk
- pelayanan
- harga

[RULES]
1. Jika pengiriman cepat tetapi barang rusak, cacat, atau pecah,
   utamakan kategori 'kualitas produk'.
2. Pilih kategori yang paling dominan dalam keluhan pelanggan.
3. Jangan membuat kategori baru.
4. Jawab HANYA dengan satu nama kategori.
5. Gunakan huruf kecil tanpa tanda baca.

[INPUT]
<review>
{ulasan_text}
</review>
"""

    else:
        raise ValueError(f"Mode '{mode}' tidak valid.")


# Preview prompt
print("\n--- DEMO 1: DYNAMIC PROMPT TEMPLATE ---")

sample_prompt = build_prompt(
    test_set[0]["ulasan"],
    mode="optimized"
)

print(sample_prompt.strip())


# ==================================================
# 3. OUTPUT NORMALIZATION
# ==================================================

def normalize_prediction(raw_output: str) -> str:
    """
    Membersihkan output model dan memastikan hasil
    termasuk kategori yang valid.
    """

    text = str(raw_output).lower().strip()

    if not text:
        return "invalid"

    first_line = text.splitlines()[0].strip()

    first_line = re.sub(
        r"^(kategori|category)\s*:\s*",
        "",
        first_line
    )

    first_line = first_line.strip(" .,:;*`#")

    if first_line in VALID_CATEGORIES:
        return first_line

    # Fallback: cari kategori dalam seluruh output
    matches = [
        category
        for category in VALID_CATEGORIES
        if re.search(
            rf"\b{re.escape(category)}\b",
            text
        )
    ]

    if len(matches) == 1:
        return matches[0]

    return "invalid"


# ==================================================
# 4. PIPELINE RUNNER
# ==================================================

def run_evaluation(test_data: list, mode: str):

    predictions = []
    request_metrics = []

    print(f"\n--- RUNNING {mode.upper()} PROMPT ---")

    for index, item in enumerate(test_data):

        prompt = build_prompt(
            item["ulasan"],
            mode=mode
        )

        start_time = time.perf_counter()

        try:

            response = client.chat(
                model=MODEL_ID,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                options={
                    "temperature": TEMPERATURE
                }
            )

            # Python-side request latency
            latency_s = time.perf_counter() - start_time

            # Ollama response
            raw_output = response.message.content.strip()

            pred_clean = normalize_prediction(raw_output)

            # Ollama token statistics
            prompt_tokens = response.prompt_eval_count or 0
            gen_tokens = response.eval_count or 0

            eval_dur_s = (
                response.eval_duration or 0
            ) / 1e9

            total_dur_s = (
                response.total_duration or 0
            ) / 1e9

            tokens_per_sec = (
                gen_tokens / eval_dur_s
                if eval_dur_s > 0
                else 0.0
            )

            request_metrics.append({
                "latency_s": latency_s,
                "total_duration_s": total_dur_s,
                "eval_duration_s": eval_dur_s,
                "prompt_tokens": prompt_tokens,
                "generated_tokens": gen_tokens,
                "tokens_per_sec": tokens_per_sec
            })

        except Exception as e:

            latency_s = time.perf_counter() - start_time

            print(f"Error data ke-{index + 1}: {e}")

            pred_clean = "error"

            request_metrics.append({
                "latency_s": latency_s,
                "total_duration_s": 0.0,
                "eval_duration_s": 0.0,
                "prompt_tokens": 0,
                "generated_tokens": 0,
                "tokens_per_sec": 0.0
            })

        predictions.append(pred_clean)

        print(
            f"[{index + 1}/{len(test_data)}] "
            f"Prediction: {pred_clean}"
        )

        time.sleep(0.2)

    return predictions, request_metrics


# ==================================================
# 5. RUN EVALUATION
# ==================================================

print("\n--- DEMO 2: PIPELINE EVALUATION ---")

preds_vague, metrics_vague = run_evaluation(
    test_set,
    mode="vague"
)

preds_optimized, metrics_optimized = run_evaluation(
    test_set,
    mode="optimized"
)


# ==================================================
# 6. CLASSIFICATION METRICS
# ==================================================

print("\n--- DEMO 3: CLASSIFICATION METRICS ---")

y_true = [
    item["ground_truth"]
    for item in test_set
]

acc_vague = accuracy_score(
    y_true,
    preds_vague
)

acc_optimized = accuracy_score(
    y_true,
    preds_optimized
)

print("\n[VAGUE PROMPT]")
print(f"Accuracy: {acc_vague * 100:.2f}%")

print(
    classification_report(
        y_true,
        preds_vague,
        labels=VALID_CATEGORIES,
        zero_division=0
    )
)

print("\n[OPTIMIZED PROMPT]")
print(f"Accuracy: {acc_optimized * 100:.2f}%")

print(
    classification_report(
        y_true,
        preds_optimized,
        labels=VALID_CATEGORIES,
        zero_division=0
    )
)


# ==================================================
# 7. A/B TESTING
# ==================================================

print("\n--- DEMO 4: A/B TESTING ---")

accuracy_difference = (
    acc_optimized - acc_vague
) * 100

print("=" * 55)
print(f"Vague Accuracy     : {acc_vague * 100:.2f}%")
print(f"Optimized Accuracy : {acc_optimized * 100:.2f}%")
print(f"Accuracy Difference: {accuracy_difference:+.2f} pp")
print("=" * 55)

print(
    f"\n{'NO':<5} | {'GROUND TRUTH':<18} | "
    f"{'VAGUE':<18} | {'OPTIMIZED':<18} | STATUS"
)

print("-" * 95)

for i, gt in enumerate(y_true):

    vague = preds_vague[i]
    optimized = preds_optimized[i]

    if vague != gt and optimized == gt:
        status = "Improved"

    elif vague == gt and optimized != gt:
        status = "Regressed"

    elif vague == gt and optimized == gt:
        status = "Both Correct"

    else:
        status = "Both Incorrect"

    print(
        f"{i+1:<5} | {gt:<18} | "
        f"{vague:<18} | {optimized:<18} | {status}"
    )


# ==================================================
# 8. BENCHMARK SUMMARY
# ==================================================

def summarize_metrics(data: list) -> dict:

    if not data:
        raise ValueError("Metrics tidak boleh kosong.")

    latencies = [m["latency_s"] for m in data]

    prompt_tokens = [m["prompt_tokens"] for m in data]

    generated_tokens = [
        m["generated_tokens"] for m in data
    ]

    total_eval_duration = sum(
        m["eval_duration_s"] for m in data
    )

    total_generated_tokens = sum(generated_tokens)

    return {
        "lat_avg": sum(latencies) / len(latencies),
        "lat_min": min(latencies),
        "lat_max": max(latencies),
        "lat_total": sum(latencies),

        "total_duration": sum(
            m["total_duration_s"] for m in data
        ),

        "prompt_total": sum(prompt_tokens),
        "prompt_avg": sum(prompt_tokens) / len(prompt_tokens),

        "gen_total": total_generated_tokens,
        "gen_avg": total_generated_tokens / len(generated_tokens),

        "tps_avg": (
            total_generated_tokens / total_eval_duration
            if total_eval_duration > 0
            else 0.0
        )
    }


sv = summarize_metrics(metrics_vague)
so = summarize_metrics(metrics_optimized)


# ==================================================
# 9. MARKDOWN EXPORT HELPERS
# ==================================================

def md_cell(text: str) -> str:

    return (
        str(text)
        .replace("|", "\\|")
        .replace("\n", " ")
        .strip()
    )


def report_to_markdown(y_true, y_pred):

    report = classification_report(
        y_true,
        y_pred,
        labels=VALID_CATEGORIES,
        output_dict=True,
        zero_division=0
    )

    lines = [
        "| Category | Precision | Recall | F1-Score | Support |",
        "|---|---:|---:|---:|---:|"
    ]

    for category in VALID_CATEGORIES:

        values = report[category]

        lines.append(
            f"| {category} "
            f"| {values['precision']:.3f} "
            f"| {values['recall']:.3f} "
            f"| {values['f1-score']:.3f} "
            f"| {int(values['support'])} |"
        )

    lines.append(
        f"| **Accuracy** | - | - "
        f"| **{accuracy_score(y_true, y_pred):.3f}** "
        f"| {len(y_true)} |"
    )

    return "\n".join(lines)


def confusion_matrix_to_markdown(
    y_true,
    y_pred,
    labels
):

    cm = confusion_matrix(
        y_true,
        y_pred,
        labels=labels
    )

    header = (
        "| Actual / Predicted | "
        + " | ".join(labels)
        + " |"
    )

    separator = "|---|" + "---:|" * len(labels)

    rows = []

    for i, label in enumerate(labels):

        rows.append(
            "| " + label + " | "
            + " | ".join(str(v) for v in cm[i])
            + " |"
        )

    return "\n".join([header, separator] + rows)


def request_metrics_to_markdown(data):

    lines = [
        "| No. | Latency (s) | Total Duration (s) "
        "| Prompt Tokens | Generated Tokens | TPS |",
        "|---:|---:|---:|---:|---:|---:|"
    ]

    for i, m in enumerate(data):

        lines.append(
            f"| {i+1} "
            f"| {m['latency_s']:.3f} "
            f"| {m['total_duration_s']:.3f} "
            f"| {m['prompt_tokens']} "
            f"| {m['generated_tokens']} "
            f"| {m['tokens_per_sec']:.2f} |"
        )

    return "\n".join(lines)


# ==================================================
# 10. GENERATE UNIFIED MARKDOWN REPORT
# ==================================================

print("\n--- EXPORTING UNIFIED REPORT ---")

extra_labels = sorted(
    set(y_true + preds_vague + preds_optimized)
    - set(VALID_CATEGORIES)
)

all_labels = VALID_CATEGORIES + extra_labels

content = f"""# Qwen Prompt Engineering Experiment

## 1. Experiment Information

| Parameter | Value |
|---|---|
| Model | {MODEL_ID} |
| Framework | Ollama Python SDK |
| Temperature | {TEMPERATURE} |
| Dataset | {JSON_FILE_PATH} |
| Total Test Samples | {len(test_set)} |
| Categories | {", ".join(VALID_CATEGORIES)} |

---

## 2. Classification Results

| No. | Ground Truth | Vague Prediction | Optimized Prediction | Status |
|---:|---|---|---|---|
"""

for i, gt in enumerate(y_true):

    vague = preds_vague[i]
    optimized = preds_optimized[i]

    if vague != gt and optimized == gt:
        status = "Improved"
    elif vague == gt and optimized != gt:
        status = "Regressed"
    elif vague == gt and optimized == gt:
        status = "Both Correct"
    else:
        status = "Both Incorrect"

    content += (
        f"| {i+1} | {md_cell(gt)} "
        f"| {md_cell(vague)} "
        f"| {md_cell(optimized)} "
        f"| {status} |\\n"
    )


content += f"""

---

## 3. Accuracy Comparison

| Metric | Vague Prompt | Optimized Prompt |
|---|---:|---:|
| Accuracy | {acc_vague * 100:.2f}% | {acc_optimized * 100:.2f}% |
| Correct Predictions | {sum(p == t for p, t in zip(preds_vague, y_true))} | {sum(p == t for p, t in zip(preds_optimized, y_true))} |
| Incorrect Predictions | {sum(p != t for p, t in zip(preds_vague, y_true))} | {sum(p != t for p, t in zip(preds_optimized, y_true))} |
| Accuracy Difference | - | {accuracy_difference:+.2f} percentage points |

---

## 4. Performance Benchmark

### 4.1 Latency & Token Summary

| Metric | Vague Prompt | Optimized Prompt |
|---|---:|---:|
| Average Latency (s) | {sv['lat_avg']:.3f} | {so['lat_avg']:.3f} |
| Minimum Latency (s) | {sv['lat_min']:.3f} | {so['lat_min']:.3f} |
| Maximum Latency (s) | {sv['lat_max']:.3f} | {so['lat_max']:.3f} |
| Total Latency (s) | {sv['lat_total']:.3f} | {so['lat_total']:.3f} |
| Total Prompt Tokens | {sv['prompt_total']} | {so['prompt_total']} |
| Average Prompt Tokens | {sv['prompt_avg']:.1f} | {so['prompt_avg']:.1f} |
| Total Generated Tokens | {sv['gen_total']} | {so['gen_total']} |
| Average Generated Tokens | {sv['gen_avg']:.1f} | {so['gen_avg']:.1f} |
| Average Generation Speed (TPS) | {sv['tps_avg']:.2f} | {so['tps_avg']:.2f} |

> Note: TPS is calculated as total generated tokens divided by total evaluation duration. Generated tokens may include reasoning tokens.

### 4.2 Vague Prompt - Individual Request

{request_metrics_to_markdown(metrics_vague)}

### 4.3 Optimized Prompt - Individual Request

{request_metrics_to_markdown(metrics_optimized)}

---

## 5. Classification Report

### 5.1 Vague Prompt

{report_to_markdown(y_true, preds_vague)}

### 5.2 Optimized Prompt

{report_to_markdown(y_true, preds_optimized)}

---

## 6. Confusion Matrix

### 6.1 Vague Prompt

{confusion_matrix_to_markdown(y_true, preds_vague, all_labels)}

### 6.2 Optimized Prompt

{confusion_matrix_to_markdown(y_true, preds_optimized, all_labels)}

---

## 7. Benchmark Conclusion

### Classification Performance

"""

if acc_optimized > acc_vague:

    content += (
        "Optimized Prompt achieved higher classification accuracy "
        "than Vague Prompt in this experiment.\\n\\n"
    )

elif acc_optimized < acc_vague:

    content += (
        "Vague Prompt achieved higher classification accuracy "
        "than Optimized Prompt in this experiment.\\n\\n"
    )

else:

    content += (
        "Both prompting strategies achieved the same "
        "classification accuracy.\\n\\n"
    )


content += f"""
### Inference Performance

- Vague Prompt average latency: {sv['lat_avg']:.3f} seconds.
- Optimized Prompt average latency: {so['lat_avg']:.3f} seconds.
- Vague Prompt generation speed: {sv['tps_avg']:.2f} tokens/s.
- Optimized Prompt generation speed: {so['tps_avg']:.2f} tokens/s.

### Final Observation

This experiment compares two prompting strategies using
the same model, dataset, and temperature configuration.

The results evaluate:

1. Classification accuracy.
2. Inference latency.
3. Prompt token consumption.
4. Generated token consumption.
5. Generation speed.

A higher classification accuracy does not necessarily
indicate faster inference.

Optimized prompts may require more input tokens and
therefore increase processing time.

---

*Generated using Ollama Python SDK.*
"""


# ==================================================
# 11. SAVE REPORT
# ==================================================

REPORT_FILE.write_text(
    content,
    encoding="utf-8"
)

print("\n" + "=" * 55)
print("EXPERIMENT COMPLETED")
print("=" * 55)

print(f"Vague Accuracy     : {acc_vague * 100:.2f}%")
print(f"Optimized Accuracy : {acc_optimized * 100:.2f}%")
print(f"Accuracy Difference: {accuracy_difference:+.2f} pp")

print("\n--- MARKDOWN EXPORT ---")
print(f"Report saved to: {REPORT_FILE}")
print(f"File size      : {REPORT_FILE.stat().st_size:,} bytes")

print("\nAll experiments and benchmarks exported successfully.")
