# LLM-Powered Q&A System for Technical Documentation

An advanced Q&A system using a fine-tuned LLM (e.g., BERT or Llama2) to answer queries from technical documentation. Features a Rust backend for performant API handling and a Python microservice for model inference.

## Features

- **Rust API** (Actix-web): Async endpoints for document upload, embedding generation, and semantic search.
- **Python ML Service** (FastAPI): Loads and serves a transformer model for embedding/text generation.
- **Vector Database**: FAISS for efficient vector similarity search.
- **Dockerized**: One-command deployment for full stack.
- **Extensible pipeline**: Add new models, document loaders, preprocessors.
- **Authentication** (JWT, optional).

## Architecture
