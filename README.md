
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
<img width="1478" height="298" alt="ss9" src="https://github.com/user-attachments/assets/524d399f-b799-4190-a87e-e7554e8a1819" />
<img width="1516" height="278" alt="ss8" src="https://github.com/user-attachments/assets/d1554785-d402-440e-a0c1-8751cb3922ed" />
<img width="1518" height="264" alt="ss7" src="https://github.com/user-attachments/assets/1a912d6c-957b-4f31-938d-bb46eb0f8a58" />
<img width="1502" height="310" alt="ss6" src="https://github.com/user-attachments/assets/edc8697e-ca84-4e59-8866-a88f850665b1" />
<img width="1404" height="276" alt="ss5" src="https://github.com/user-attachments/assets/0e45e235-0eec-48ee-82ac-339c358d6e64" />
<img width="1514" height="276" alt="ss4" src="https://github.com/user-attachments/assets/577e327e-58b7-4cf2-b944-468542427ad0" />
<img width="1513" height="498" alt="ss3" src="https://github.com/user-attachments/assets/bf1904d1-3215-454e-9851-fbc6519a574c" />
<img width="1457" height="269" alt="ss2" src="https://github.com/user-attachments/assets/90aee164-7b1c-4b25-bf0e-e5a7e453014f" />
<img width="1474" height="444" alt="SS1" src="https://github.com/user-attachments/assets/ba8e362f-85eb-41b6-a9d2-715a6ebfe0cd" />
