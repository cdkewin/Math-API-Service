import asyncio
from app.logic import fibonacci

queue = None


async def init_worker():
    global queue
    if queue is None:
        queue = asyncio.Queue()
        asyncio.create_task(worker_loop())


async def worker_loop():
    while True:
        n, future = await queue.get()
        result = fibonacci(n)
        future.set_result(result)


async def fib_worker(n: int) -> int:
    global queue
    if queue is None :
        await init_worker()
    future = asyncio.get_event_loop().create_future()
    await queue.put((n, future))
    return await future
