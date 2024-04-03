import os

import psycopg2
from psycopg2.extras import execute_values

DB_USER = os.environ.get("POSTGRES_USER")
DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
DB_PORT = os.environ.get("POSTGRES_PORT")
DB_NAME = os.environ.get("POSTGRES_DB")
DB_HOST = "marketdb"


def execute_query(query, params=None):
    with psycopg2.connect(
        database=DB_HOST,
        user=DB_USER,
        host=DB_HOST,
        password=DB_PASSWORD,
        port=DB_PORT,
    ) as conn:
        cur = conn.cursor()
        cur.execute(query, params)
        rows = cur.fetchall()
        return rows


def execute_insert_query(query, params=None):
    with psycopg2.connect(
        database=DB_HOST,
        user=DB_USER,
        host=DB_HOST,
        password=DB_PASSWORD,
        port=DB_PORT,
    ) as conn:
        cur = conn.cursor()
        cur.execute(query, params)
        conn.commit()
        return cur.fetchone()[0]


def execute_multiple_insert_queries(query, params_arr=None):
    with psycopg2.connect(
        database=DB_HOST,
        user=DB_USER,
        host=DB_HOST,
        password=DB_PASSWORD,
        port=DB_PORT,
    ) as conn:
        cur = conn.cursor()
        execute_values(cur, query, params_arr)
        conn.commit()


def get_customers():
    rows = execute_query("SELECT * FROM customer")
    return rows


def get_orders_of_customer(customer_id):
    rows = execute_query(
        """
        SELECT 
            item.name, 
            item.description, 
            item.price, 
            item.price*order_items.quantity
        FROM orders 
        JOIN order_items 
        ON 
            order_items.order_id = orders.id 
        JOIN item
        ON 
            item.id = order_items.item_id
        WHERE
            orders.customer_id=%(customer_id)s
        """,
        {"customer_id": customer_id},
    )
    return rows


def get_total_cost_of_an_order(order_id):
    rows = execute_query(
        """
        SELECT 
            SUM(item.price*order_items.quantity)
        FROM orders 
        JOIN order_items 
        ON 
            order_items.order_id = orders.id 
        JOIN item 
        ON 
            item.id = order_items.item_id
        WHERE
            orders.id=%(order_id)s
        """,
        {"order_id": order_id},
    )
    return {"Order Total": rows[0][0]}


def get_orders_between_dates(after, before):
    rows = execute_query(
        """
        SELECT
            customer.name,
            item.name, 
            item.price, 
            item.price*order_items.quantity
        FROM orders 
        JOIN customer
        ON
            customer.id = orders.customer_id
        JOIN order_items 
        ON 
            order_items.order_id = orders.id 
        JOIN item 
        ON 
            item.id = order_items.item_id
        WHERE
            orders.order_time >= %(after)s
        AND
            orders.order_time <= %(before)s
        """,
        {"after": after, "before": before},
    )
    return rows


def insert_order_items(order_id, item_id, quantity):
    try:
        execute_insert_query(
            """
            INSERT INTO order_items
            VALUES
                (%(order_id)s, %(item_id)s, %(quantity)s)
            """,
            {"order_id": order_id, "item_id": item_id, "quantity": quantity},
        )
        return True

    except Exception:
        return False


def add_new_order_for_customer(customer_id, items):
    try:
        new_order_id = execute_insert_query(
            """
            INSERT INTO orders
            (customer_id, order_time)
            VALUES
                (%(customer_id)s, NOW())
            RETURNING id
            """,
            {"customer_id": customer_id},
        )

        (
            execute_multiple_insert_queries(
                """
            INSERT INTO order_items
            (order_id, item_id, quantity)
            VALUES %s
            """,
                [
                    (new_order_id, item["id"], item["quantity"])
                    for item in items
                ],
            )
        )

        return True

    except Exception:
        return False
