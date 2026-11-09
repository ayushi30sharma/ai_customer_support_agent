<img width="1457" height="269" alt="ss2" src="https://github.com/user-attachments/assets/fdbace47-d2de-42cc-9179-ef4844f854d9" />
<img width="1474" height="444" alt="SS1" src="https://github.com/user-attachments/assets/2bcd6d59-51fc-423e-a16c-70132ecc9f21" />

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

