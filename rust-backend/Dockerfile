FROM rust:1.81 as builder

WORKDIR /app
COPY . .

RUN cargo build --release

FROM debian:bookworm-slim
WORKDIR /app
COPY --from=builder /app/target/release/llm_qa_backend /app/llm_qa_backend

# (Optional) Add CA certificates if needed for HTTPS
RUN apt-get update && apt-get install -y ca-certificates && rm -rf /var/lib/apt/lists/*

ENV RUST_LOG=info
EXPOSE 8080

CMD ["/app/llm_qa_backend"]