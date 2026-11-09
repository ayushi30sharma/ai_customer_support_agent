# 🤖 AI-Powered E-Commerce Customer Support Agent

An enterprise-grade, secure, and observable AI customer support agent for an e-commerce store. Built with **Gemini**, **LangGraph**, and **FastAPI**, this agent handles order inquiries, processes returns, searches store policies, and escalates to humans when necessary.

## 🏗️ System Architecture

```text
Customer 
   │
   ▼
[Streamlit Frontend] (Chat UI + Agent Activity Panel)
   │
   ▼
[FastAPI Backend] (REST API & Session Management)
   │
   ▼
[LangGraph Workflow] 
   ├── Input Guardrails (PII Masking, Distress Detection)
   ├── Agent Node (Google Gemini 2.5/3.6 Flash)
   └── Tool Node (Strict Python Business Logic)
         │
         ├── [PostgreSQL] (Customers, Orders, Returns)
         └── [ChromaDB]   (Vector Store for Store Policies)

<img width="1478" height="298" alt="ss9" src="https://github.com/user-attachments/assets/21c02d72-2dd8-4f11-9327-77eecc13ddbb" />
