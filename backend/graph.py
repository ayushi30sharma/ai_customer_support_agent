"""
LangGraph Workflow: The orchestrator.
"""
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, ToolMessage, SystemMessage

from backend.state import AgentState
from backend.agent import llm_with_tools, tools_list
from backend.prompts import SYSTEM_PROMPT
from backend.guardrails import detect_distress
from backend.tools import escalate_to_human as py_escalate_to_human

tools_by_name = {t.name: t for t in tools_list}

def guardrail_node(state: AgentState):
    last_message = state["messages"][-1].content
    if detect_distress(last_message):
        py_escalate_to_human(state["conversation_id"], state["customer_id"], "Customer distress detected")
        return {"is_escalated": True, "escalation_reason": "Customer distress"}
    return {}

def agent_node(state: AgentState):
    # Inject the customer ID into the system prompt so the AI knows who it's talking to
    system_context = f"\n\n[SYSTEM CONTEXT: The authenticated customer's ID is {state['customer_id']}. NEVER ask the user for their ID.]"
    messages = [SystemMessage(content=SYSTEM_PROMPT + system_context)] + state["messages"]
    
    if state.get("is_escalated"):
        messages.append(SystemMessage(content="You have escalated this to a human. Tell the customer a human will contact them shortly. Do not call any more tools."))
    
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

def tool_node(state: AgentState):
    tool_calls = state["messages"][-1].tool_calls
    results = []
    
    for tool_call in tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        
        try:
            tool_func = tools_by_name[tool_name]
            # Inject the state into the tool execution for InjectedState
            result = tool_func.invoke({**tool_args, "state": state})
        except Exception as e:
            result = f"Tool execution failed: {str(e)}"
            
        results.append(ToolMessage(content=str(result), tool_call_id=tool_call["id"]))
    
    return {"messages": results, "tool_calls_made": state.get("tool_calls_made", 0) + len(tool_calls)}

def should_continue(state: AgentState):
    last_message = state["messages"][-1]
    if state.get("is_escalated"):
        return "end"
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        return "tools"
    return "end"

workflow = StateGraph(AgentState)
workflow.add_node("guardrail", guardrail_node)
workflow.add_node("agent", agent_node)
workflow.add_node("tools", tool_node)

workflow.set_entry_point("guardrail")
workflow.add_edge("guardrail", "agent")
workflow.add_conditional_edges("agent", should_continue, {"tools": "tools", "end": END})
workflow.add_edge("tools", "agent")

# Add memory
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)