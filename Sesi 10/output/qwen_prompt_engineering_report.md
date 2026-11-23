# Qwen Prompt Engineering Experiment

## 1. Experiment Information

| Parameter | Value |
|---|---|
| Model | qwen3.8:27b-mlx |
| Framework | Ollama Python SDK |
| Temperature | 0.0 |
| Dataset | dataset_test.json |
| Total Test Samples | 3 |
| Categories | pengiriman, kualitas produk, pelayanan, harga |

---

## 2. Classification Results

| No. | Ground Truth | Vague Prediction | Optimized Prediction | Status |
|---:|---|---|---|---|
| 1 | pengiriman | pengiriman | pengiriman | Both Correct |\n| 2 | kualitas produk | kualitas produk | kualitas produk | Both Correct |\n| 3 | harga | invalid | harga | Improved |\n

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
| Average Latency (s) | 47.810 | 27.952 |
| Minimum Latency (s) | 43.815 | 13.679 |
| Maximum Latency (s) | 50.093 | 42.347 |
| Total Latency (s) | 143.430 | 83.855 |
| Total Prompt Tokens | 92 | 483 |
| Average Prompt Tokens | 30.7 | 161.0 |
| Total Generated Tokens | 1306 | 1014 |
| Average Generated Tokens | 435.3 | 338.0 |
| Average Generation Speed (TPS) | 10.35 | 13.10 |

> Note: TPS is calculated as total generated tokens divided by total evaluation duration. Generated tokens may include reasoning tokens.

### 4.2 Vague Prompt - Individual Request

| No. | Latency (s) | Total Duration (s) | Prompt Tokens | Generated Tokens | TPS |
|---:|---:|---:|---:|---:|---:|
| 1 | 49.522 | 49.510 | 27 | 341 | 10.08 |
| 2 | 50.093 | 50.076 | 29 | 512 | 10.39 |
| 3 | 43.815 | 43.793 | 36 | 453 | 10.50 |

### 4.3 Optimized Prompt - Individual Request

| No. | Latency (s) | Total Duration (s) | Prompt Tokens | Generated Tokens | TPS |
|---:|---:|---:|---:|---:|---:|
| 1 | 27.828 | 27.814 | 158 | 300 | 12.03 |
| 2 | 13.679 | 13.670 | 159 | 163 | 15.15 |
| 3 | 42.347 | 42.338 | 166 | 551 | 13.20 |

---

## 5. Classification Report

### 5.1 Vague Prompt

| Category | Precision | Recall | F1-Score | Support |
|---|---:|---:|---:|---:|
| pengiriman | 1.000 | 1.000 | 1.000 | 1 |
| kualitas produk | 1.000 | 1.000 | 1.000 | 1 |
| pelayanan | 0.000 | 0.000 | 0.000 | 0 |
| harga | 0.000 | 0.000 | 0.000 | 1 |
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
| kualitas produk | 0 | 1 | 0 | 0 | 0 |
| pelayanan | 0 | 0 | 0 | 0 | 0 |
| harga | 0 | 0 | 0 | 0 | 1 |
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

- Vague Prompt average latency: 47.810 seconds.
- Optimized Prompt average latency: 27.952 seconds.
- Vague Prompt generation speed: 10.35 tokens/s.
- Optimized Prompt generation speed: 13.10 tokens/s.

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
