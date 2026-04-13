Payment LLM Reconciliation Engine

A hybrid LLM-powered financial intelligence system for parsing, querying, and reconciling SWIFT MT103 payment messages.

This project explores how LLM systems should be designed for financial workflows — combining deterministic logic with semantic retrieval instead of relying purely on embeddings.
-----------------------------------------------------------------------------------------------------------------------
🚀 Overview

Financial systems require:

Numeric precision

Currency sensitivity

Deterministic validation

Explainability

Pure vector similarity is insufficient for these constraints.
--------------------------------------------------------------------------------------------------------------------

🚀 Features
🔍 MT103 Parsing — Extracts transaction data from SWIFT messages
⚖️ Reconciliation Engine
Exact Match
Partial Match (tolerance-based)
Mismatch detection
📊 Reconciliation Summary API
🔎 Semantic Search — Query transactions using natural language
🧠 RAG Pipeline
Vector database (ChromaDB)
Embeddings (Sentence Transformers)
Local LLM (Ollama - Llama3)
⚡ FastAPI Backend

---------------------------------------------------------------------------------------------------------------------
🏗️ Architecture

This project implements a hybrid retrieval architecture:

MT103 File
   ↓
Parser (MT Parser)
   ↓
Structured Transactions
   ↓
Reconciliation Engine
   ↓
Exact / Partial / Mismatch
   ↓
Vector DB (Chroma)
   ↓
Retriever
   ↓
Local LLM (Ollama)
   ↓
Explanation API
      

-----------------------------------------------------------------------------------------------------------------------
🧠 Architecture
1️⃣ MT103 Parsing Layer

Extracts SWIFT {4:} blocks

Parses fields:

:20: Transaction Reference

:32A: Value Date + Currency + Amount

:50K: Ordering Customer

:59: Beneficiary

Handles:

Multi-line fields

Comma-based decimal amounts

Real-world message formatting

-----------------------------------------------------------------------------------------------------------------------

2️⃣ Embedding Layer

Model: all-MiniLM-L6-v2

Vector DB: Chroma

Converts structured transactions into semantic representations

Enables similarity-based retrieval

---------------------------------------------------------------------------------------------------------------------

3️⃣ Hybrid Query Engine

Instead of relying purely on embeddings:

Structured filtering (currency, sender, amount tolerance)

Optional semantic ranking

Deterministic numeric validation

Example query:

Payment from OMEGA LTD for GBP 5400

Pipeline:

Extract structured constraints

Apply rule-based filtering

Return exact matched transaction

---------------------------------------------------------------------------------------------------------------------------

4️⃣ API Layer

Built using FastAPI.

Endpoints:

Endpoint	                        Description
/health	                        Service status
/search	                        Semantic vector search
/smart-search	                  Hybrid structured query engine
/reconcile	(WIP)                   Ledger reconciliation
/reconciliation-summary             recon-summary
/reconciliation-summary            recon-summary-with-llm

----------------------------------------------------------------------------------------------------------------------------

🛠 Tech Stack

Python

FastAPI

SentenceTransformers

ChromaDB

Pandas

Custom MT103 parser

---------------------------------------------------------------------------------------------------------------------

🔎 Why Hybrid Retrieval?

In financial systems:

Numeric values must match precisely

Currency mismatches are critical

Semantic similarity alone is unsafe

This project demonstrates:

Hybrid Retrieval = Deterministic Filtering + AI Assistance

This mirrors real-world fintech AI system design.

----------------------------------------------------------------------------------------------------------------------

📦 Installation
git clone https://github.com/Nikhil1601/payment_llm_recon_engine/tree/main

python -m venv venv
venv\Scripts\activate

pip install -r requirement.txt

Run API:

uvicorn api.main:app --reload

Visit:

http://127.0.0.1:8000/docs

-----------------------------------------------------------------------------------------------------------------------

🎯 Motivation

Most LLM demos ignore financial constraints.

This project explores how to build AI systems that are:

Structured

Deterministic where required

AI-assisted where useful

Production-oriented

-------------------------------------------------------------------------------------------------------------------


