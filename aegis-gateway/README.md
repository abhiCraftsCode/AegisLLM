# 🛡️ AegisLLM — Enterprise Security Gateway & Guardrail System

[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![ONNX Runtime](https://img.shields.io/badge/ONNX_Runtime-1.17-005CED?logo=onnx)](https://onnxruntime.ai/)
[![DistilBERT](https://img.shields.io/badge/Transformers-DistilBERT-yellow)](https://huggingface.co/distilbert-base-uncased)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An open-source, API-first security reverse proxy designed to inspect, sanitize, and block adversarial Prompt Injections, Jailbreaking, and System Prompt Leakage before reaching production LLM endpoints.

---

## ⚡ Key Highlights

- **Sub-15ms Latency Overhead:** Exported to hardware-accelerated ONNX binaries for fast CPU inference without requiring dedicated GPUs.
- **3-Tier Threat Inspection:** Microsecond regex heuristics + Fine-tuned DistilBERT classification + LiteLLM proxy routing.
- **Drop-in OpenAI Compatibility:** Exposes `/v1/chat/completions` for zero-friction integration.
- **Client SDK:** Lightweight JavaScript wrapper (`aegis-guard`) providing 3-line integration.

---

## 🏗️ Architecture Flow

User Prompt ──► [ SDK (aegis-guard) ] ──► [ FastAPI Proxy Gateway ]
│
┌───────────┴───────────┐
▼ ▼
[ Tier 1: Regex ] [ Tier 2: ONNX Model ]
│ │
└───────────┬───────────┘
▼
┌───────────────────────┐
▼ ▼
[ If Malicious ] [ If Safe ]
Return HTTP 403 Proxy to Target LLM

---

## 🚀 Quickstart

### 1. Clone & Install Dependencies

```bash
git clone [https://github.com/](https://github.com/)<your-username>/aegis-llm.git
cd aegis-llm
pip install -r requirements.txt
python export_onnx.py
uvicorn main:app --reload --port 8000
node test_client.js
```
