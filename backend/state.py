"""
Conversation State for LangGraph.
"""
from typing import Annotated, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    # The `add_messages` reducer tells LangGraph to append new messages
    # to the list rather than overwriting them.
    messages: Annotated[list[BaseMessage], add_messages]
    
    # Customer context
    customer_id: str
    conversation_id: str
    
    # Security & Escalation flags
    is_escalated: bool
    escalation_reason: str
    
    # Tracking
    tool_calls_made: int
    return_created_id: str