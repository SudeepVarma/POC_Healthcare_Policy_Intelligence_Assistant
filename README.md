# POC_Healthcare_Policy_Intelligence_Assistant
Designed to demonstrate enterprise document intelligence workflows applicable to healthcare analytics, coding compliance, reimbursement policy analysis, and payer-provider content management.
# Enterprise Healthcare Content Intelligence (Proof of Concept)

A lightweight proof of concept demonstrating **Healthcare Content Intelligence** using **Retrieval-Augmented Generation (RAG)** and **local Large Language Models (LLMs)**.

The application ingests healthcare policy documents, performs semantic retrieval, extracts structured information, compares policy revisions, and converts narrative policies into executable Python rules.

> **Note:** This project is a hackathon-style research prototype developed for a Research Engineer internship assessment. It is intended to demonstrate concepts rather than serve as a production-ready healthcare application.
> 
---

## Features

- PDF document upload and parsing
- Retrieval-Augmented Generation (RAG)
- Local inference using Ollama (Llama 3.1)
- ChromaDB vector database
- Semantic document search
- Structured JSON extraction using Pydantic
- Policy comparison
- Policy-to-Code transformation
- Rule validation sandbox

---
## Prerequisites

- Python 3.10+
- Ollama
- Llama 3.1 model

Install the model:

```bash
ollama pull llama3.1:8b
```

Install Python dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Application

Start the Ollama server:

```bash
ollama serve
```

Launch the Streamlit application:

```bash
streamlit run app.py
```

The application will be available at:

```
http://localhost:8501
```

---

## Technology Stack

- Python
- Streamlit
- Ollama
- Llama 3.1
- ChromaDB
- Sentence Transformers
- PyMuPDF
- Pydantic

---

## Disclaimer

This project is intended solely as a proof of concept for demonstrating AI-assisted healthcare document intelligence. It should not be used for clinical decision-making, medical coding, claims adjudication, or regulatory compliance without appropriate validation and human oversight.
