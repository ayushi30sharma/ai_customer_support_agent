"""
Guardrails: The safety layer for the agent.
Runs BEFORE the LLM sees the message, and AFTER the tool returns data.
"""
import re

# --- 1. PII Masking ---
def mask_card(text: str) -> str:
    """Mask credit card numbers (13-16 digits, optional spaces/dashes)."""
    pattern = r'\b(?:\d[ -]*?){13,16}\b'
    return re.sub(pattern, '[CARD REDACTED]', text)

def mask_phone(text: str) -> str:
    """Mask standard 10-digit phone numbers, optionally with country code."""
    # This regex specifically looks for 10 digits, optionally preceded by +91 or similar
    pattern = r'(\+?\d{1,3}[-.\s]?)?\b\d{10}\b'
    return re.sub(pattern, '[PHONE REDACTED]', text)

def sanitize_output(text: str) -> str:
    """Run all PII masking on any text before sending to the customer."""
    text = mask_card(text)   # Card FIRST (so it doesn't get chopped up by phone regex)
    text = mask_phone(text)  # Phone SECOND
    return text

# --- 2. Distress & Escalation Detection ---
def detect_distress(text: str) -> bool:
    """
    Detects if a customer is angry or explicitly asks for a human.
    If True, the workflow will bypass tools and escalate immediately.
    """
    text_lower = text.lower()
    
    triggers = [
        "human", "agent", "representative", "manager", "speak to someone",
        "angry", "furious", "terrible", "worst", "sue", "lawyer",
        "scam", "fraud", "useless"
    ]
    
    for word in triggers:
        if word in text_lower:
            return True
    return False

# --- 3. Prompt Injection Defense ---
def sanitize_policy_text(text: str) -> str:
    """
    Strips prompt injection attempts from retrieved policy documents.
    """
    injection_phrases = [
        "ignore previous instructions", "ignore all rules", 
        "you are now", "system prompt", "bypass", "override"
    ]
    text_lower = text.lower()
    for phrase in injection_phrases:
        if phrase in text_lower:
            return "[POLICY BLOCKED: Potential prompt injection detected]"
    return text

# --- 4. Out of Scope Check (Basic) ---
def is_in_scope(text: str) -> bool:
    """
    Checks if the user is asking something completely unrelated to e-commerce.
    """
    off_topic = ["write a poem", "python code", "who is the president", "recipe"]
    text_lower = text.lower()
    return not any(topic in text_lower for topic in off_topic)