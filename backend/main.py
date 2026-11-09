"""
FastAPI Backend.
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from langgraph.errors import GraphRecursionError
import traceback

from backend.graph import app as agent_app
from backend.database import get_order_with_details, fetch_one

api = FastAPI(title="E-Commerce AI Support API")

class ChatRequest(BaseModel):
    message: str
    customer_id: str
    conversation_id: str

class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    tools_used: int
    escalated: bool

@api.get("/health")
def health_check():
    return {"status": "ok"}

@api.post("/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    config = {"configurable": {"thread_id": req.conversation_id}, "recursion_limit": 8}
    
    # Check if conversation exists
    state = await agent_app.aget_state(config)
    inputs = {"messages": [HumanMessage(content=req.message)]}
    
    # Initialize state for a new conversation
    if not state.values:
        inputs.update({
            "customer_id": req.customer_id,
            "conversation_id": req.conversation_id,
            "is_escalated": False,
            "escalation_reason": "",
            "tool_calls_made": 0,
            "return_created_id": ""
        })

    try:
        # Run the agent
        result = await agent_app.ainvoke(inputs, config=config)
        
        final_message_obj = result["messages"][-1]
        final_text = final_message_obj.content
        
        # Handle Gemini's list-of-blocks response format
        if isinstance(final_text, list):
            final_text = " ".join([block.get("text", "") for block in final_text if isinstance(block, dict)])
        
        final_text = str(final_text)

        return ChatResponse(
            response=final_text,
            conversation_id=req.conversation_id,
            tools_used=result.get("tool_calls_made", 0),
            escalated=result.get("is_escalated", False)
        )

    except GraphRecursionError:
        return ChatResponse(
            response="I'm sorry, I'm having trouble processing this request right now. Let me connect you to a human support agent.",
            conversation_id=req.conversation_id,
            tools_used=8,
            escalated=True
        )
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@api.get("/orders/{order_id}")
def get_order(order_id: str):
    order = get_order_with_details(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@api.get("/returns/{return_id}")
def get_return(return_id: str):
    ret = fetch_one("SELECT * FROM returns WHERE return_id = %s", (return_id,))
    if not ret:
        raise HTTPException(status_code=404, detail="Return not found")
    return ret