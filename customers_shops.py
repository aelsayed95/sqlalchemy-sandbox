import asyncio
from dataclasses import dataclass, field
import random
import time

ITEMS = ["milk", "eggs", "crepes", "rice", "bread", "tomatoes", "cucumbers", "fish", "chicken", "shrimp"]

@dataclass
class Order:
    created: float = field(init=False)
    item: str

    def __post_init__(self):
        self.created = time.perf_counter()


async def place_order(cid: int, q: asyncio.Queue):
    n = random.randint(0, 5)
    for i in range(0, n):
        await asyncio.sleep(1)
        item_id = random.randint(0, len(ITEMS) - 1)
        print(f"Customer id={cid} placed an order for {ITEMS[item_id]}")
        order = Order(ITEMS[item_id])
        await q.put(order)
        print(f"Customer id={cid}'s order={order} successfully sent")

async def process_orders(shop_id: int, q: asyncio.Queue):
    while True:
        print(f"Shop id={shop_id} ready to receive orders")
        order = await q.get()
        print(f"Shop id={shop_id} processing order={order}")
        await asyncio.sleep(1)

        now = time.perf_counter()
        print(f"Shop id={shop_id} processed order={order} in {now - order.created:0.5f}")
        q.task_done()
    # TODO how to run this
    print(f"Shop id={shop_id} closing for the day.")

async def main():
    q = asyncio.Queue()
    customers = [asyncio.create_task(place_order(n, q)) for n in range(5)]
    shops = [asyncio.create_task(process_orders(n, q)) for n in range(5)]

    await asyncio.gather(*customers)
    await q.join()  # awaits shops too

    for shop in shops:
        shop.cancel()

if __name__ == "__main__":
    asyncio.run(main())
