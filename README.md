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
```
# EVALUATION QUESTIONS

<img width="1474" height="444" alt="SS1" src="https://github.com/user-attachments/assets/9803acd3-dfdf-444c-b7fb-00452eb94a2c" />
<img width="1457" height="269" alt="ss2" src="https://github.com/user-attachments/assets/cbe5588a-c644-4dcb-beb4-60f19f40b774" />
<img width="1513" height="498" alt="ss3" src="https://github.com/user-attachments/assets/b372ec1f-d9dc-4584-b232-d791dd4c64a1" />
<img width="1514" height="276" alt="ss4" src="https://github.com/user-attachments/assets/c3f5b18f-1a01-4437-ae83-4a9efcb3f02e" />
<img width="1404" height="276" alt="ss5" src="https://github.com/user-attachments/assets/fdfbb7be-1973-435f-8832-b8d74c46f782" />
<img width="1502" height="310" alt="ss6" src="https://github.com/user-attachments/assets/8fdf2da1-dfc2-40a5-adf0-6c714d27a8a3" />
<img width="1518" height="264" alt="ss7" src="https://github.com/user-attachments/assets/4e042704-747f-4150-ae6d-95fcfd71a81a" />
<img width="1516" height="278" alt="ss8" src="https://github.com/user-attachments/assets/1f6c72e7-14f4-40c6-8e3d-60d912b44d22" />
<img width="1478" height="298" alt="ss9" src="https://github.com/user-attachments/assets/34c3ed19-4edd-488b-845f-50ca49e52659" />

