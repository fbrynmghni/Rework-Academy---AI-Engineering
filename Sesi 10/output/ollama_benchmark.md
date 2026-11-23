# Ollama Model Performance Benchmark

## Model Information

- **Model:** gpt-oss:20b
- **Runtime:** Ollama Python SDK
- **Date:** 15-11-2026 13:02:46
- **Total Demos:** 4

---

## 1. Execution Performance


| Demo | Wall Time | Ollama Total | Load Time | Prompt Eval | Generation | Tokens | Tokens/sec |
|---|---:|---:|---:|---:|---:|---:|---:|
| Demo 1 - System Instruction | 13.652 s | 13.646 s | 1.829 s | 0.740 s | 11.070 s | 299 | 27.010 tok/s |
| Demo 2 - Hyperparameter Tuning | 4.107 s | 4.104 s | 0.002 s | 0.669 s | 3.428 s | 94 | 27.422 tok/s |
| Demo 3 - Native JSON Mode | 10.670 s | 10.665 s | 0.003 s | 0.761 s | 9.894 s | 265 | 26.785 tok/s |
| Demo 4 - Strict Schema Enforcement (Pydantic) | 15.327 s | 15.325 s | 0.002 s | 0.633 s | 14.680 s | 376 | 25.612 tok/s |


---

## 2. Performance Summary

| Metric | Result |
|---|---:|
| Total Python Wall Time (API calls) | 43.755 s |
| Total Ollama Duration | 43.741 s |
| Total Generated Tokens | 1034 |
| Number of Model Requests | 4 |

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

1. All demos use model `gpt-oss:20b`.
2. Model parameters may affect generation speed.
3. First execution may include model loading time.
4. Performance can vary depending on system resources,
   available RAM, and concurrent processes.
5. Wall Time and Ollama Total Duration are different
   measurements and should not be added together.

---

*Generated automatically using Python and Ollama.*
