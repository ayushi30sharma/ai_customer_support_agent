<img width="1478" height="298" alt="ss9" src="https://github.com/user-attachments/assets/79be35ba-c89a-4b4b-95e1-3572296a7b2c" />
<img width="1516" height="278" alt="ss8" src="https://github.com/user-attachments/assets/b40f029a-9377-45bb-a0a6-cdb737c373cd" />
<img width="1518" height="264" alt="ss7" src="https://github.com/user-attachments/assets/0b902407-7417-4936-89d7-5911075c2355" />
<img width="1502" height="310" alt="ss6" src="https://github.com/user-attachments/assets/8cdb117f-99b9-4f9a-acb0-1ddbbb86dd12" />
<img width="1404" height="276" alt="ss5" src="https://github.com/user-attachments/assets/bb20b869-02d0-4dfc-9d23-cb84880eccea" />
<img width="1514" height="276" alt="ss4" src="https://github.com/user-attachments/assets/41dce077-2f70-4cfa-823a-ff27002d9b4e" />
<img width="1513" height="498" alt="ss3" src="https://github.com/user-attachments/assets/cdbb8cb3-ba78-40a3-a72c-5468ae16a596" />
<img width="1457" height="269" alt="ss2" src="https://github.com/user-attachments/assets/b6480001-9be3-44b3-b10e-f9df1e049b52" />
<img width="1474" height="444" alt="SS1" src="https://github.com/user-attachments/assets/5838f466-29e3-4dda-a0dd-7cace2e429fd" />
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

