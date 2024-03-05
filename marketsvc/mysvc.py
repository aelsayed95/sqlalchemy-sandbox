import os
import psycopg2

DB_USER = os.environ.get("POSTGRES_USER")
DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
DB_PORT = os.environ.get("POSTGRES_PORT")
DB_NAME = os.environ.get("POSTGRES_DB")
DB_HOST = "marketdb"


def execute_query(query):
    with psycopg2.connect(database = DB_HOST, 
                        user = DB_USER, 
                        host = DB_HOST,
                        password = DB_PASSWORD,
                        port = DB_PORT) as conn:
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        conn.commit()

    return rows

def get_customers():
    rows = execute_query("SELECT * FROM customer")
    for row in rows:
        print(row)

def get_orders_of_customer(customer_id):
    rows = execute_query(f"SELECT * FROM orders WHERE customer_id={customer_id}")
    for row in rows:
        print(row)

def get_items_in_store():
    rows = execute_query("SELECT store.id, item.name, store.price FROM store JOIN item ON store.item_id = item.id")
    for row in rows:
        print(row)

if __name__ == "__main__":
    # get_customers()
    # get_orders_of_customer(1)
    get_items_in_store()

