[Evaluation Questions.pdf](https://github.com/user-attachments/files/34633953/Evaluation.Questions.pdf)
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

