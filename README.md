# AI-Powered E-Commerce Customer Support Agent

An AI agent that handles customer queries (order status, returns,
refunds, escalations) using Gemini + LangGraph, with a Streamlit
chat UI and FastAPI backend.

**Status:** 🚧 Under construction — Phase 0 complete.

## Quickstart

1. Copy `.env.example` → `.env` and add your Gemini key.
2. Create a virtual environment and install dependencies.
3. (Phases 1–8 will fill in the rest.)

## Architecture

Customer → Streamlit → FastAPI → LangGraph + Gemini → Tools
                                                        ↓
                                                    SQLite + ChromaDB



                                                    
