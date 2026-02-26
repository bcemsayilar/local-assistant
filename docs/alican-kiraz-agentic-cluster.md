# Alican Kiraz - Virtual Agentic Developer Team

Kaynak: Twitter/X postu

## Proje Konsepti
Local LLM inference + agentic orchestration altyapisi. "Virtual Coding Cluster / Agentic Developer Team" mimarisi. 7/24 kapali devre gelistirme ortami.

## Donanim Altyapisi
| Cihaz | Adet | RAM | Rol |
|-------|------|-----|-----|
| M3 Ultra Mac Studio | 1 | 512GB Unified | Ana inference (DA VINCI - Qwen3.5-397B) |
| M4 Mac Mini | 4 | 16GB | Agent execution / orchestration |
| NVIDIA DGX Spark | 2 | 128GB | GPU inference (TESLA - Dual RTX 5090, Coder Pool) |
| Raspberry Pi 5 | 2 | 8GB | Hafif gorevler |
| 24-port switch | 1 | - | Network backbone |

## Mimari (Diyagramdan)

### Node'lar
- **DA VINCI** (10.0.42.10) - M3 Ultra, Reasoning LLM / Qwen3.5-397B. Reasoning & Review rolu.
- **VON NEUMANN** (10.0.42.20) - Qwen3.5-397B MLX + Qwen3-Coder-Next vLLM FP8. Hem inference hem coding.
- **SHANNON** (10.0.42.21) - Qwen3-Coder-Next vLLM FP8. Coding node.
- **TESLA** (Desktop PC, Dual RTX 5090) - GPU-0 (8001) + GPU-1 (8002). Coder Pool.
- **OpenClaw Agent Farm** (10.0.42.40) - Docker container'lar ile agent calistirma.

### Orchestration
- **FastAPI Router Proxy** - Merkezi gorev yonlendirme
- **Nginx Load Balancer** (10.0.42.40:8080) - GPU node'lari arasinda yuk dagilimi
- **11 Autonomous Developer Agents**:
  - Coder Agents (6x)
  - Tech Lead (1x)
  - Tech Writer (1x)
  - QA Engineer (1x)
  - (diger roller)

### Infrastructure Katmani
- Task API
- Monitoring & Logging
- CI/CD Tool
- Metrics & Cost Tracking
- Monorepo with task & code pipeline

## Kullanilan Modeller
- Qwen3.5-397B (reasoning, review)
- Qwen3-Coder-Next (coding, vLLM FP8 quantization)
- MLX framework (Apple Silicon optimizasyonu)

## Bizim Icin Notlar
- Qwen3.5-397B 512GB unified RAM'de calisiyor - bizim 8GB ile kiyaslanamaz ama mimari fikirleri uyarlanabilir
- FastAPI Router Proxy kavrami ilginc - bizde de Ollama onune proxy konabilir
- Rol bazli agent ayirimi (Tech Lead, QA, Coder) - multi-agent workflow icin referans
- OpenClaw kullanmis agent farm icin - arastir
- vLLM FP8 quantization - NVIDIA GPU'larda verimli inference
- Kapali devre ag yapisi - bizimle ayni felsefe (privacy-first, no cloud)
