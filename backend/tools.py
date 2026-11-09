"""
The 5 core tools for the AI Agent.
Notice: There is zero AI in this file. This is pure, deterministic Python.
The LLM will select these tools, but Python executes them and enforces the rules.
"""
from datetime import date
from typing import Any
import random

from backend.database import (
    fetch_one, fetch_all, execute, demo_today,
    get_order_with_details, get_product, get_returns_for_order
)
from backend.guardrails import sanitize_output
from backend.policy_retriever import search_policy as chroma_search_policy


# ==========================================
# TOOL 1: Get Order Status
# ==========================================
def get_order_status(order_id: str, authenticated_customer_id: str) -> dict[str, Any]:
    """
    Retrieve order details. Requires ownership verification (POL011).
    """
    order = get_order_with_details(order_id)
    if not order:
        return {"error": f"Order {order_id} not found."}
    
    # POL011: Ownership Verification
    if order["customer_id"] != authenticated_customer_id:
        return {"error": "Unauthorized: This order does not belong to your account."}
    
    # Sanitize output just in case
    return {
        "order_id": order["order_id"],
        "product_name": order["product_name"],
        "order_date": str(order["order_date"]),
        "delivery_date": str(order["delivery_date"]) if order["delivery_date"] else "Not delivered yet",
        "order_status": order["order_status"],
        "payment_status": order["payment_status"],
        "payment_method": order["payment_method"],
        "total_amount_inr": order["total_amount_inr"]
    }


# ==========================================
# TOOL 2: Search Policy
# ==========================================
def search_policies(query: str) -> str:
    """
    Search the ChromaDB policy database for the most relevant rules.
    """
    results = chroma_search_policy(query, top_k=2)
    if not results:
        return "No specific policy found for this query."
    
    # Combine the top 2 results into a single string for the LLM
    combined_text = "\n\n".join([r["text"] for r in results])
    return sanitize_output(combined_text)


# ==========================================
# TOOL 3: Check Return Eligibility
# ==========================================
def check_return_eligibility(order_id: str, authenticated_customer_id: str) -> dict[str, Any]:
    """
    The core business rule engine. Determines if a return is allowed.
    Applies POL001, POL003, POL004, POL006, POL008.
    """
    order = get_order_with_details(order_id)
    if not order:
        return {"eligible": False, "reason": f"Order {order_id} not found."}

    # POL011: Ownership
    if order["customer_id"] != authenticated_customer_id:
        return {"eligible": False, "reason": "Unauthorized: This order is not yours."}

    # POL008: Not Delivered
    if order["order_status"] != "Delivered" or not order["delivery_date"]:
        return {"eligible": False, "reason": "Order is not yet delivered. Returns cannot be initiated."}

    # POL004: Duplicate Return
    existing_returns = get_returns_for_order(order_id)
    if existing_returns:
        ret = existing_returns[0]
        return {
            "eligible": False, 
            "reason": f"A return already exists for this order (ID: {ret['return_id']}, Status: {ret['return_status']})."
        }

    # POL003: Non-Returnable Product
    if not order["returnable"]:
        return {"eligible": False, "reason": f"The product '{order['product_name']}' is non-returnable."}

    # POL001: 7-Day Window
    # delivery_date from psycopg2 might be a string or a date object. Handle both.
    if isinstance(order["delivery_date"], str):
        delivery_date = date.fromisoformat(order["delivery_date"])
    else:
        delivery_date = order["delivery_date"]
        
    days_since_delivery = (demo_today() - delivery_date).days
    if days_since_delivery > 7:
        return {"eligible": False, "reason": f"Return window expired. Delivered {days_since_delivery} days ago (max 7)."}

    # POL006: High-Value Escalation (> 5000 INR)
    requires_human = False
    if order["total_amount_inr"] > 5000:
        requires_human = True

    return {
        "eligible": True,
        "reason": f"Eligible (Delivered {days_since_delivery} days ago).",
        "requires_escalation": requires_human,
        "order_details": order
    }


# ==========================================
# TOOL 4: Create Return
# ==========================================
def create_return(order_id: str, authenticated_customer_id: str, reason: str) -> dict[str, Any]:
    """
    Creates a return in Postgres. Re-validates eligibility to prevent bypassing.
    """
    # 1. Re-validate rules (Never trust the LLM)
    check = check_return_eligibility(order_id, authenticated_customer_id)
    if not check["eligible"]:
        return {"error": f"Cannot create return: {check['reason']}"}
    
    if check.get("requires_escalation"):
        return {"error": "This is a high-value refund. It requires human approval and cannot be automated."}

    # 2. Generate Return ID
    # In a real system, use a UUID. For demo, we do RET3001, RET3002, etc.
    max_ret = fetch_one("SELECT MAX(return_id) as max_id FROM returns")
    if max_ret and max_ret["max_id"]:
        num = int(max_ret["max_id"].replace("RET", "")) + 1
    else:
        num = 3001
    new_return_id = f"RET{num}"

    # 3. Insert into Database
    amount = check["order_details"]["total_amount_inr"]
    today_str = demo_today().isoformat()
    
    execute(
        """
        INSERT INTO returns (return_id, order_id, customer_id, request_date, reason, return_status, refund_status, refund_amount_inr)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (new_return_id, order_id, authenticated_customer_id, today_str, reason, "Pending", "Pending", amount)
    )

    return {
        "status": "success",
        "return_id": new_return_id,
        "message": f"Return created successfully. Return ID: {new_return_id}. Refund of ₹{amount} will be processed after item inspection."
    }


# ==========================================
# TOOL 5: Escalate to Human
# ==========================================
def escalate_to_human(conversation_id: str, customer_id: str, reason: str) -> dict[str, Any]:
    """
    Logs an escalation. The AI will use the returned message to tell the user.
    """
    # In a production app, this would create a ticket in Zendesk/Freshdesk.
    # Here, we just simulate a successful handover log.
    print(f"🚨 ESCALATION: Conv: {conversation_id}, Cust: {customer_id}, Reason: {reason}")
    
    return {
        "status": "escalated",
        "message": "I have escalated this issue to our human support team. They will review your case and contact you via email shortly."
    }