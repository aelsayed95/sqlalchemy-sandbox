import asyncio

async def worker(job):
    for i in range(10):
        print(f"'{job}' in progress...")
        await asyncio.sleep(1)
    print(f"'{job}' done.")

async def main():
    jobs = ["order milk", "order apples", "order vegetables"]
    await asyncio.gather(*[worker(job) for job in jobs])

if __name__ == "__main__":
    asyncio.run(main())
