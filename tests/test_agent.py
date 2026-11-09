"""
Automated tests for the core business logic.
Run with: pytest tests/test_agent.py -v
"""
import pytest
from backend.tools import check_return_eligibility, get_order_status

# Scenario 3: Return within window
def test_return_within_window():
    result = check_return_eligibility("ORD5002", "C1002")
    assert result["eligible"] is True
    assert result["requires_escalation"] is False

# Scenario 4: Return outside window (POL001)
def test_return_outside_window():
    result = check_return_eligibility("ORD5001", "C1001")
    assert result["eligible"] is False
    assert "expired" in result["reason"].lower()

# Scenario 5: Non-returnable product (POL003)
def test_non_returnable_product():
    result = check_return_eligibility("ORD5005", "C1005")
    assert result["eligible"] is False
    assert "non-returnable" in result["reason"].lower()

# Scenario 6: Undelivered order (POL008)
def test_undelivered_order():
    result = check_return_eligibility("ORD5003", "C1003")
    assert result["eligible"] is False
    assert "not yet delivered" in result["reason"].lower()

# Scenario 7: Duplicate return (POL004)
def test_duplicate_return():
    result = check_return_eligibility("ORD5006", "C1006")
    assert result["eligible"] is False
    assert "already exists" in result["reason"].lower()

# Scenario 9: High-value refund escalation (POL006)
def test_high_value_escalation():
    result = check_return_eligibility("ORD5011", "C1004")
    assert result["eligible"] is True
    assert result["requires_escalation"] is True

# Scenario 11: Cross-customer authorization (POL011)
def test_cross_customer_access():
    result = get_order_status("ORD5001", "C1002") # C1002 trying to view C1001's order
    assert "error" in result
    assert "unauthorized" in result["error"].lower()