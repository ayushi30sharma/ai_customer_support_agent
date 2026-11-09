"""
Streamlit Frontend.
A clean chat interface that talks to the FastAPI backend.
"""
import streamlit as st
import requests
import uuid

# The URL of our FastAPI backend
BACKEND_URL = "http://localhost:8000"

st.set_page_config(page_title="AI Support Agent", page_icon="🤖", layout="wide")

st.title("🤖 E-Commerce AI Support")

# --- Sidebar: User Selection & Reset ---
with st.sidebar:
    st.header("Customer Context")
    
    # 1. Get the selected customer
    selected_customer = st.selectbox(
        "Select Customer ID (Demo)", 
        ["C1001", "C1002", "C1003", "C1004", "C1005", "C1006", "C1007", "C1008"]
    )
    
    # 2. If the customer changes, wipe the memory and start fresh!
    if "current_customer" not in st.session_state:
        st.session_state.current_customer = selected_customer
        st.session_state.conversation_id = str(uuid.uuid4())
        st.session_state.messages = []
        
    if st.session_state.current_customer != selected_customer:
        # User switched accounts. Wipe chat and session.
        st.session_state.current_customer = selected_customer
        st.session_state.conversation_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.rerun()

    st.text(f"Session ID: {st.session_state.conversation_id[:8]}...")
    
    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.session_state.conversation_id = str(uuid.uuid4())
        st.rerun()

# --- Main Chat Interface ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Accept new user input
if prompt := st.chat_input("Ask about your order, returns, or policies..."):
    # 1. Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Call FastAPI Backend
    with st.chat_message("assistant"):
        with st.spinner("Agent is thinking..."):
            try:
                payload = {
                    "message": prompt,
                    "customer_id": st.session_state.current_customer, # <--- THE FIX IS HERE
                    "conversation_id": st.session_state.conversation_id
                }
                # Added timeout so it doesn't hang forever if the backend crashes
                res = requests.post(f"{BACKEND_URL}/chat", json=payload, timeout=60)
                res.raise_for_status()
                data = res.json()
                
                # 3. Display AI response
                st.markdown(data["response"])
                st.session_state.messages.append({"role": "assistant", "content": data["response"]})
                
                # 4. Display Agent Metadata (Activity Panel)
                with st.expander("🛠️ Agent Activity Details"):
                    st.write(f"**Tools Used:** {data['tools_used']}")
                    st.write(f"**Escalated to Human:** {data['escalated']}")
                    
            except Exception as e:
                st.error(f"Error connecting to backend: {e}")
                st.info("Make sure the FastAPI backend is running (`uvicorn backend.main:api --reload`).")