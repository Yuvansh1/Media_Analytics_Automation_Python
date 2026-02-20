# 🏦 Insurance Customer Support RAG Assistant

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Production--Ready-green)
![Pinecone](https://img.shields.io/badge/VectorDB-Pinecone-purple)
![Gemini](https://img.shields.io/badge/LLM-Gemini-orange)
![RAG](https://img.shields.io/badge/Architecture-RAG-red)
![Docker](https://img.shields.io/badge/Containerized-Docker-blue)
![Status](https://img.shields.io/badge/Status-Active-success)

Enterprise grade Retrieval Augmented Generation system for insurance customer support.

Built using:

* Gemini Embeddings
* Gemini LLM
* Pinecone Serverless Vector Index
* FastAPI REST API
* Docker Containerization

---

## 🚀 Problem Statement

Insurance support teams handle high volumes of repetitive queries:

* Does my policy cover flood damage?
* What is included in auto insurance?
* How do I file a claim?
* Is water damage covered?

Manual lookup increases handling time and operational cost.

This project implements a scalable RAG architecture to provide context grounded AI responses from policy documents.

---

# 🧠 Architecture Diagram

```
                  ┌────────────────────┐
                  │      User Query     │
                  └──────────┬─────────┘
                             │
                             ▼
                 ┌──────────────────────┐
                 │ Gemini Embedding API │
                 └──────────┬───────────┘
                            │ 1536-dim vector
                            ▼
               ┌──────────────────────────┐
               │ Pinecone Vector Database │
               │ Namespace: insurance_support │
               └──────────┬───────────────┘
                          │ Top-K Results
                          ▼
                ┌──────────────────────┐
                │ Gemini LLM (Flash)   │
                │ Context-grounded Gen │
                └──────────┬───────────┘
                           ▼
                  ┌─────────────────┐
                  │  FastAPI Layer  │
                  └──────────┬──────┘
                             ▼
                      JSON Response
```

---

# 🏗 System Design

## 1️⃣ Embedding Layer

* Model: `gemini-embedding-001`
* Output dimension: 1536
* L2 normalized for cosine similarity
* Optimized for Pinecone cosine metric alignment

---

## 2️⃣ Vector Storage

* Pinecone Serverless Index
* Metric: Cosine similarity
* Namespace isolation
* Horizontally scalable
* Metadata stored for contextual grounding

---

## 3️⃣ Retrieval Layer

* Top K semantic similarity search
* Namespace filtered queries
* Context aggregation from metadata
* Deterministic context injection

---

## 4️⃣ Generation Layer

* Model: `gemini-2.5-flash`
* Strict context constrained prompting
* Hallucination minimized through grounding

---

## 5️⃣ API Layer

* FastAPI
* REST endpoint: `/ask`
* Swagger auto documentation at `/docs`
* Stateless microservice design

---

# 📂 Project Structure

```
insurance_rag_assistant/
│
├── main.py
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .env
├── requirements.txt
├── README.md
└── .gitignore
```

---

# 🔐 Environment Variables

Create `.env`:

```
PINECONE_API_KEY=your_key
GEMINI_API_KEY=your_key
```

---

# ⚙️ Local Setup

### Install Dependencies

```
pip install -r requirements.txt
```

### Run Application

```
uvicorn main:app --reload
```

### Swagger UI

```
http://127.0.0.1:8000/docs
```

---

# 🐳 Docker Deployment

Containerized deployment ensures environment consistency and cloud readiness.

## Build Docker Image

```
pip freeze > requirements.txt

docker build -t insurance-rag .
```

## Run Container

```
docker run -p 8000:8000 --env-file .env insurance-rag
```

Access API:

```
http://localhost:8000/docs
```

---

## 🐳 Docker Compose Deployment

For cleaner environment variable handling:

```
docker compose up --build
```
Open in your Browser:

```
http://localhost:8000/docs

```

from your local environment.

---

# 🔎 Example Query

```
Does home insurance cover flooding?
```
## 📸 Project Preview

![Insurance RAG Architecture](fast_api_output.png)

System flow:

1. Embed query
2. Retrieve top matching clauses
3. Inject contextual metadata
4. Generate grounded answer
5. Return structured JSON

---

# 📈 Enterprise Features

* Namespace based index partitioning
* Embedding normalization alignment
* Context constrained LLM generation
* Stateless API microservice
* Docker containerization
* Production safe environment variable management
* Modular architecture design

---

# 🚀 Scalability Considerations

* Bulk ingestion pipeline for policy PDFs
* Async embedding pipeline
* Fraud detection extension
* Claims similarity search
* Horizontal scaling via Pinecone serverless
* Kubernetes deployable container
* CI/CD ready

---

# 💼 Portfolio Value

Demonstrates:

* Vector database architecture
* End to end RAG system design
* Embedding engineering
* Prompt grounding strategies
* API microservice architecture
* Containerized AI deployment
* Production deployment patterns
