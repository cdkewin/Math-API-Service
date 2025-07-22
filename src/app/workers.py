import asyncio
from app.logic import fibonacci

queue = asyncio.Queue()


def init_worker():
    asyncio.create_task(worker_loop())


async def worker_loop():
    while True:
        n, future = await queue.get()
        result = fibonacci(n)
        future.set_result(result)


async def fib_worker(n: int) -> int:
    loop = asyncio.get_event_loop()
    future = loop.create_future()
    await queue.put((n, future))
    return await future
