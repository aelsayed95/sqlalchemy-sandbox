# Reference: https://docs.python.org/3/glossary.html#term-asynchronous-iterator

import asyncio
import time


async def dispatch_orders(delay):
    print(f"Started dispatching at {time.strftime('%X')}")
    for i in range(delay):
        await asyncio.sleep(1)
        yield i
    print(f"Done dispatching at {time.strftime('%X')}")


async def deliver_order(order):
    await asyncio.sleep(1)
    print(f"order {order} delivered {time.strftime('%X')}")


async def main():
    deliveries = []
    async for order in dispatch_orders(5):
        print(f"order {order} dispatched.")

    # TODO: uncomment this
    #     deliver_task = asyncio.create_task(deliver_order(order))
    #     deliveries.append(deliver_task)

    # await asyncio.gather(*deliveries)


asyncio.run(main())
