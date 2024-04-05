from db.base import engine
from sqlalchemy import text


def execute_query(query, params=None):
    with engine.connect() as conn:
        result = conn.execute(text(query), params)

        return [row._asdict() for row in result]


def execute_insert_query(query, params=None):
    with engine.connect() as conn:
        result = conn.execute(text(query), params)
        conn.commit()

        return [row._asdict() for row in result]


def execute_insert_queries(query, params_list=None):
    with engine.connect() as conn:
        conn.execute(text(query), params_list)
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
            item.price*order_items.quantity AS total
        FROM orders 
        JOIN order_items 
        ON 
            order_items.order_id = orders.id 
        JOIN item 
        ON 
            item.id = order_items.item_id
        WHERE
            orders.customer_id=:customer_id
        """,
        {"customer_id": customer_id},
    )
    return rows


def get_total_cost_of_an_order(order_id):
    rows = execute_query(
        """
        SELECT 
            SUM(item.price*order_items.quantity) AS order_total
        FROM orders 
        JOIN order_items 
        ON 
            order_items.order_id = orders.id 
        JOIN item 
        ON 
            item.id = order_items.item_id
        WHERE
            orders.id=:order_id
        """,
        {"order_id": order_id},
    )
    return rows[0]


def get_orders_between_dates(after, before):
    rows = execute_query(
        """
        SELECT
            customer.name,
            item.name, 
            item.price, 
            item.price*order_items.quantity AS total
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
            orders.order_time >= :after
        AND
            orders.order_time <= :before
        """,
        {"after": after, "before": before},
    )
    return rows


def add_new_order_for_customer(customer_id, items):
    try:
        new_order_id = execute_insert_query(
            """
            INSERT INTO orders
                (customer_id, order_time)
            VALUES
                (:customer_id, NOW())
            RETURNING id
            """,
            {"customer_id": customer_id},
        )[0]["id"]

        (
            execute_insert_queries(
                """
            INSERT INTO order_items
                (order_id, item_id, quantity)
            VALUES
                (:order_id, :item_id, :quantity)
            """,
                [
                    {
                        "order_id": new_order_id,
                        "item_id": item["id"],
                        "quantity": item["quantity"],
                    }
                    for item in items
                ],
            )
        )
        return True

    except Exception:
        return False
