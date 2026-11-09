"""
Agent Configuration: Defines the LLM and wraps our pure Python tools 
into LangChain-compatible tools using InjectedState.
"""
from typing import Annotated
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langgraph.prebuilt import InjectedState
from dotenv import load_dotenv

from backend.tools import (
    get_order_status as py_get_order_status,
    search_policies as py_search_policies,
    check_return_eligibility as py_check_return_eligibility,
    create_return as py_create_return,
    escalate_to_human as py_escalate_to_human
)

load_dotenv()

# Change model name if you hit 503s or 429s
llm = ChatGoogleGenerativeAI(model="gemini-3.6-flash")

@tool
def get_order_status(order_id: str, state: Annotated[dict, InjectedState]) -> str:
    """Get the status, delivery date, and payment info for an order."""
    result = py_get_order_status(order_id, state["customer_id"])
    return json.dumps(result, default=str)

@tool
def search_policies(query: str) -> str:
    """Search the store's return and refund policy database."""
    return py_search_policies(query)

@tool
def check_return_eligibility(order_id: str, state: Annotated[dict, InjectedState]) -> str:
    """Check if an order is eligible for return based on store rules."""
    result = py_check_return_eligibility(order_id, state["customer_id"])
    if "order_details" in result:
        del result["order_details"]
    return json.dumps(result, default=str)

@tool
def create_return(order_id: str, reason: str, state: Annotated[dict, InjectedState]) -> str:
    """Create a return request in the database."""
    result = py_create_return(order_id, state["customer_id"], reason)
    return json.dumps(result, default=str)

@tool
def escalate_to_human(reason: str, state: Annotated[dict, InjectedState]) -> str:
    """Escalate the conversation to a human support agent."""
    result = py_escalate_to_human(state["conversation_id"], state["customer_id"], reason)
    return json.dumps(result, default=str)

tools_list = [
    get_order_status, search_policies, check_return_eligibility, 
    create_return, escalate_to_human
]
llm_with_tools = llm.bind_tools(tools_list)