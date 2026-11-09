"""
Safe PostgreSQL access layer.
"""
import os
from contextlib import contextmanager
from datetime import date
from typing import Optional

import psycopg2
import psycopg2.extras
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "").strip()
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set in .env")

def demo_today() -> date:
    """Freeze 'today' using DEMO_TODAY env var so demos never break."""
    demo = os.getenv("DEMO_TODAY", "").strip()
    if demo:
        return date.fromisoformat(demo)
    return date.today()

@contextmanager
def get_connection():
    conn = psycopg2.connect(DATABASE_URL)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def fetch_one(sql: str, params: tuple = ()) -> Optional[dict]:
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(sql, params)
            row = cur.fetchone()
            return dict(row) if row else None

def fetch_all(sql: str, params: tuple = ()) -> list[dict]:
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(sql, params)
            return [dict(r) for r in cur.fetchall()]

def execute(sql: str, params: tuple = ()) -> int:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            return cur.rowcount

# ---------- Domain Helpers ----------

def get_customer(customer_id: str) -> Optional[dict]:
    return fetch_one("SELECT * FROM customers WHERE customer_id = %s", (customer_id,))

def get_order(order_id: str) -> Optional[dict]:
    return fetch_one("SELECT * FROM orders WHERE order_id = %s", (order_id,))

def get_product(product_id: str) -> Optional[dict]:
    p = fetch_one("SELECT * FROM products WHERE product_id = %s", (product_id,))
    if p:
        p["returnable"] = bool(p["returnable"])
    return p

def get_returns_for_order(order_id: str) -> list[dict]:
    return fetch_all("SELECT * FROM returns WHERE order_id = %s ORDER BY request_date", (order_id,))

def get_order_with_details(order_id: str) -> Optional[dict]:
    row = fetch_one(
        """
        SELECT 
            o.order_id, o.customer_id, o.product_id, o.quantity,
            o.order_date, o.delivery_date, o.order_status,
            o.payment_status, o.payment_method, o.total_amount_inr,
            p.product_name, p.returnable,
            c.full_name AS customer_name
        FROM orders o
        JOIN products p  ON o.product_id  = p.product_id
        JOIN customers c ON o.customer_id = c.customer_id
        WHERE o.order_id = %s
        """,
        (order_id,)
    )
    if row:
        row["returnable"] = bool(row["returnable"])
    return row