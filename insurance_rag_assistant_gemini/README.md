# 🏦 Insurance Customer Support RAG Assistant

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Production--Ready-green)
![Pinecone](https://img.shields.io/badge/VectorDB-Pinecone-purple)
![Gemini](https://img.shields.io/badge/LLM-Gemini-orange)
![RAG](https://img.shields.io/badge/Architecture-RAG-red)
![Status](https://img.shields.io/badge/Status-Active-success)

Enterprise grade Retrieval Augmented Generation system for insurance customer support.

Built using:

* Gemini Embeddings
* Gemini LLM
* Pinecone Serverless Vector Index
* FastAPI REST API

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
               │  Namespace: insurance    │
               └──────────┬───────────────┘
                          │ Top-K Results
                          ▼
                ┌──────────────────────┐
                │ Gemini LLM (Flash)   │
                │ Context-grounded Gen │
                └──────────┬───────────┘
                           ▼
                  ┌─────────────────┐
                  │  Final Response │
                  └─────────────────┘
```

---

# 🏗 System Design

## 1️⃣ Embedding Layer

* Model: `gemini-embedding-001`
* Output dimension: 1536
* Normalized for cosine similarity
* Compatible with Pinecone serverless index

## 2️⃣ Vector Storage

* Pinecone Serverless Index
* Metric: Cosine similarity
* Namespace based isolation
* Scalable to millions of policy clauses

## 3️⃣ Retrieval Layer

* Top K similarity search
* Namespace filtered
* Metadata preserved for context injection

## 4️⃣ Generation Layer

* Gemini 2.5 Flash
* Prompt grounded in retrieved context
* No external hallucinated knowledge

## 5️⃣ API Layer

* FastAPI
* Swagger documentation
* REST endpoint: `/ask`

---

# 📂 Project Structure

```
insurance_rag_assistant/
│
├── main.py
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

# ⚙️ Setup

### Install

```
pip install -r requirements.txt
```

### Run

```
uvicorn main:app --reload
```

### Swagger UI

```
http://127.0.0.1:8000/docs
```

---

# 🔎 Example Query

```
Does home insurance cover flooding?
```

System:

* Embeds query
* Retrieves relevant clauses
* Generates grounded response
* Returns JSON

---

# 📈 Enterprise Features

* Namespace based index partitioning
* Embedding dimensional alignment
* Context constrained generation
* API level deployment
* Modular architecture
* Production safe environment variables

---

# 🚀 Scalability Considerations

* Can ingest large policy datasets
* Extendable to fraud detection
* Extendable to claims similarity search
* Horizontal scaling via Pinecone serverless
* Deployable via Docker / Kubernetes

---

# 💼 Portfolio Value

Demonstrates:

* Vector database architecture
* RAG system design
* Embedding optimization
* LLM prompt grounding
* API engineering
* Production deployment patterns

---

# 🔮 Roadmap

* PDF ingestion pipeline
* Claim similarity clustering
* Fraud anomaly detection
* Role based authentication
* Observability and logging
* CI/CD integration