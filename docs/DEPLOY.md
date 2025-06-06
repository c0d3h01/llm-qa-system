# Deploying LLM-QA System

## Prerequisites

- Docker + Docker Compose
- At least 8GB RAM for local inference
- Pre-indexed FAISS vectors and doc mapping (see instructions below)

## Local Setup

1. Clone the repo:
    ```
    git clone https://github.com/c0d3h01/llm-qa-system.git
    cd llm-qa-system
    ```

2. Prepare your documentation corpus:
    - Place your raw docs (txt/pdf/md) in `data/raw/`.
    - Use the provided script (`scripts/build_index.py`) to create FAISS index and docs.txt.

3. Build and start:
    ```
    docker compose up --build
    ```

4. Test the API:
    ```
    curl -X POST http://localhost:8080/api/query -d '{"question": "What is OAuth2?"}' -H "Content-Type: application/json"
    ```

See [../README.md](../README.md) for more details.

## Production

- Mount external persistent volumes for `data/`
- Secure API with JWT (see Rust backend)
- Use NGINX as reverse proxy for HTTPS
- Monitor containers (Prometheus/Grafana)