# GPT-OSS Prompt Engineering Experiment

## 1. Experiment Information

| Parameter | Value |
|---|---|
| Model | gpt-oss:20b |
| Framework | Ollama Python SDK |
| Temperature | 0.0 |
| Dataset | dataset_test.json |
| Total Test Samples | 3 |
| Categories | pengiriman, kualitas produk, pelayanan, harga |

---

## 2. Classification Results

| No. | Ground Truth | Vague Prediction | Optimized Prediction | Status |
|---:|---|---|---|---|
| 1 | pengiriman | pengiriman | pengiriman | Both Correct |\n| 2 | kualitas produk | invalid | kualitas produk | Improved |\n| 3 | harga | harga | harga | Both Correct |\n

---

## 3. Accuracy Comparison

| Metric | Vague Prompt | Optimized Prompt |
|---|---:|---:|
| Accuracy | 66.67% | 100.00% |
| Correct Predictions | 2 | 3 |
| Incorrect Predictions | 1 | 0 |
| Accuracy Difference | - | +33.33 percentage points |

---

## 4. Performance Benchmark

### 4.1 Latency & Token Summary

| Metric | Vague Prompt | Optimized Prompt |
|---|---:|---:|
| Average Latency (s) | 7.746 | 7.977 |
| Minimum Latency (s) | 4.741 | 3.890 |
| Maximum Latency (s) | 12.363 | 16.125 |
| Total Latency (s) | 23.239 | 23.931 |
| Total Prompt Tokens | 268 | 656 |
| Average Prompt Tokens | 89.3 | 218.7 |
| Total Generated Tokens | 524 | 560 |
| Average Generated Tokens | 174.7 | 186.7 |
| Average Generation Speed (TPS) | 26.32 | 25.03 |

> Note: TPS is calculated as total generated tokens divided by total evaluation duration. Generated tokens may include reasoning tokens.

### 4.2 Vague Prompt - Individual Request

| No. | Latency (s) | Total Duration (s) | Prompt Tokens | Generated Tokens | TPS |
|---:|---:|---:|---:|---:|---:|
| 1 | 6.135 | 6.131 | 86 | 99 | 26.40 |
| 2 | 4.741 | 4.737 | 90 | 113 | 26.48 |
| 3 | 12.363 | 12.360 | 92 | 312 | 26.23 |

### 4.3 Optimized Prompt - Individual Request

| No. | Latency (s) | Total Duration (s) | Prompt Tokens | Generated Tokens | TPS |
|---:|---:|---:|---:|---:|---:|
| 1 | 16.125 | 16.119 | 216 | 389 | 25.33 |
| 2 | 3.890 | 3.884 | 219 | 82 | 23.23 |
| 3 | 3.916 | 3.914 | 221 | 89 | 25.53 |

---

## 5. Classification Report

### 5.1 Vague Prompt

| Category | Precision | Recall | F1-Score | Support |
|---|---:|---:|---:|---:|
| pengiriman | 1.000 | 1.000 | 1.000 | 1 |
| kualitas produk | 0.000 | 0.000 | 0.000 | 1 |
| pelayanan | 0.000 | 0.000 | 0.000 | 0 |
| harga | 1.000 | 1.000 | 1.000 | 1 |
| **Accuracy** | - | - | **0.667** | 3 |

### 5.2 Optimized Prompt

| Category | Precision | Recall | F1-Score | Support |
|---|---:|---:|---:|---:|
| pengiriman | 1.000 | 1.000 | 1.000 | 1 |
| kualitas produk | 1.000 | 1.000 | 1.000 | 1 |
| pelayanan | 0.000 | 0.000 | 0.000 | 0 |
| harga | 1.000 | 1.000 | 1.000 | 1 |
| **Accuracy** | - | - | **1.000** | 3 |

---

## 6. Confusion Matrix

### 6.1 Vague Prompt

| Actual / Predicted | pengiriman | kualitas produk | pelayanan | harga | invalid |
|---|---:|---:|---:|---:|---:|
| pengiriman | 1 | 0 | 0 | 0 | 0 |
| kualitas produk | 0 | 0 | 0 | 0 | 1 |
| pelayanan | 0 | 0 | 0 | 0 | 0 |
| harga | 0 | 0 | 0 | 1 | 0 |
| invalid | 0 | 0 | 0 | 0 | 0 |

### 6.2 Optimized Prompt

| Actual / Predicted | pengiriman | kualitas produk | pelayanan | harga | invalid |
|---|---:|---:|---:|---:|---:|
| pengiriman | 1 | 0 | 0 | 0 | 0 |
| kualitas produk | 0 | 1 | 0 | 0 | 0 |
| pelayanan | 0 | 0 | 0 | 0 | 0 |
| harga | 0 | 0 | 0 | 1 | 0 |
| invalid | 0 | 0 | 0 | 0 | 0 |

---

## 7. Benchmark Conclusion

### Classification Performance

Optimized Prompt achieved higher classification accuracy than Vague Prompt in this experiment.\n\n
### Inference Performance

- Vague Prompt average latency: 7.746 seconds.
- Optimized Prompt average latency: 7.977 seconds.
- Vague Prompt generation speed: 26.32 tokens/s.
- Optimized Prompt generation speed: 25.03 tokens/s.

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
