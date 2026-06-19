# Automating Cybersecurity Compliance Reports with Generative AI

Final Year Project, BSc. (Hons.) Computer Science, University College Dublin.

A prototype system that ingests authentication and network telemetry, computes deterministic compliance metrics, and uses Retrieval-Augmented Generation (RAG) to produce draft cybersecurity compliance reports aligned with the EU NIS2 Directive (Article 21, Access Control) and ISO/IEC 27001 control A.9.

**Author:** Bohdan Myronenko (22209140)
**Supervisor:** Dr. Shen Wang
**Institution:** UCD School of Computer Science

---

## What this project does

Cybersecurity compliance reporting under NIS2, the Cyber Resilience Act, and the AI Act demands that technical telemetry (logs, IAM configs, network records) be translated into formal regulatory language. That translation step is manual, time-consuming, and inconsistent, especially for SMEs.

This system automates the drafting step. It:

1. Ingests heterogeneous logs (CSV authentication data, system logs, Zeek network telemetry).
2. Normalises records into a common ECS-inspired schema.
3. Computes compliance metrics deterministically over a streaming accumulator (failure rates, MFA coverage, repeated-failure source IPs, attack indicators, and so on).
4. Retrieves relevant regulatory text from a FAISS-indexed knowledge base of NIS2 articles and ISO control summaries.
5. Generates a structured Markdown compliance report through a grounded LLM pipeline, with severity-tagged findings, evidence linkage, and recommendations.

Every numeric claim in the output is traceable back to either a computed metric or a retrieved regulation chunk. The system supports both a privacy-preserving local deployment (Ollama) and external API benchmarking.

## Architecture

Five containerised services orchestrated via Docker Compose, separated across private and public networks:

| Service | Role |
|---------|------|
| **WebUI** (Streamlit) | Log upload, format onboarding, report generation, RAG-augmented chat |
| **API gateway** (FastAPI) | Stable client-facing endpoints, proxies to worker |
| **Worker** (FastAPI) | Ingestion, normalisation, metrics, RAG indexing, agent execution, report synthesis |
| **Ollama** | Local LLM inference and embeddings (privacy-preserving mode) |
| **Redis** | Approved format configs, metric definitions, historical baselines |

The pipeline is deliberately split: deterministic ETL handles all numeric work, and the LLM only generates the narrative layer on top of pre-computed metrics. This separation makes evaluation across different LLM providers an apples-to-apples comparison.

## Quick start

### Prerequisites

- Docker and Docker Compose
- Approximately 16 GB RAM recommended for local LLM inference
- GPU optional, but improves latency for the local model profile

### Running the system

```bash
git clone https://csgitlab.ucd.ie/22209140/cybersec-compliance.git
cd cybersec-compliance

# Copy and edit environment configuration
cp removemyname.env .env
# Edit .env to set API_MODE (LOCAL or EXTERNAL) and any API keys

# Build and start all services
docker compose up -d --build

# Pull the local LLM model into Ollama (first run only)
docker compose exec ollama ollama pull llama3.1:8b
docker compose exec ollama ollama pull nomic-embed-text
```

Once running, access the WebUI at `http://localhost:8501`.

### Generating a report

1. Open the WebUI and check service health on the landing page.
2. Upload a log file (RBA CSV, Zeek log, or other supported format).
3. If the format is unrecognised, the schema-inference agent will propose ECS field mappings for your approval.
4. Trigger report generation. The Markdown output is written to `/out` and surfaced in the UI.

## Configuration

Runtime configuration is controlled through environment variables in `.env`.

Switch between local and cloud inference by changing `API_MODE` and restarting the worker. No other configuration changes are required.

## Datasets

The system was developed and evaluated against three open datasets:

- **Risk-Based Authentication (RBA)** — Kaggle authentication logs with attack-IP and account-takeover labels. Primary development dataset.
- **LogHub / LogHub-2.0** — system log corpus for parser benchmarking.
- **UWF ZeekData22** — annotated Zeek network telemetry.

Place datasets under `/data` (mapped via Docker volume). The format sniffer prioritises known headers; you can also force a format through environment variables for controlled evaluation runs.

## Key design decisions

Two early decisions shaped the architecture:

1. **RAG over fine-tuning.** A preliminary LoRA fine-tuning experiment on Qwen2.5-1.5B with a small NIS2 dataset on consumer GPU hardware produced hallucinated regulatory content (conflating NIS2 with GDPR, fabricating requirements). This negative result motivated the move to retrieval-augmented generation, which grounds outputs in actual regulation text without requiring training infrastructure.

2. **Deterministic metrics + generative narration.** The streaming accumulator computes identical metrics regardless of which LLM runs. Only the narrative and insight-generation layers vary between providers. This separation is what makes auditable reporting and fair cross-model evaluation possible.

## Limitations

- Currently scoped to NIS2 Article 21 (Access Control) and ISO 27001 A.9. Other compliance domains (incident reporting, supply-chain security) require knowledge-base extension and additional metric definitions.
- The local LLM (LLaMA 3.1:8b) shows lower JSON parse reliability and higher cross-run variability than cloud models. The system's heuristic fallback ensures reports are still produced, but operators relying purely on local inference should expect occasional retries.
- Reports are drafts. They require expert review before submission to regulators.

## Ethical considerations

The fluency of LLM-generated text can create a false sense of completeness. This system is explicitly designed to produce **draft** documentation that requires human validation. Confidence scores are surfaced in the chat interface, AI-generated content is clearly labelled, and the human-in-the-loop agent design ensures no AI-proposed schema or metric definition affects the pipeline without explicit operator approval.

When `API_MODE=EXTERNAL`, log data is transmitted to third-party APIs. Operators should ensure appropriate sanitisation and that usage complies with GDPR and any internal data-handling policies. The `LOCAL` mode processes everything on-premise via Ollama and does not transmit telemetry externally.

## Acknowledgements

Thanks to Dr. Shen Wang for supervision throughout this project, and to the maintainers of the open datasets and tools this work builds on, including LogHub, the RBA dataset authors, FAISS, Ollama, and the Hugging Face ecosystem.

## References

Key sources informing this work:

- Directive (EU) 2022/2555 — NIS2 Directive
- Regulation (EU) 2024/2847 — Cyber Resilience Act
- Regulation (EU) 2024/1689 — AI Act
- ISO/IEC 27001:2022 Annex A.9 — Access Control
- Lewis et al. (2020), *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*
- Hu et al. (2021), *LoRA: Low-Rank Adaptation of Large Language Models*
- Zheng et al. (2023), *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena*

Full bibliography is in the project thesis.
