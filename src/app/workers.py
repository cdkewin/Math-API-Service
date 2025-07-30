import asyncio
from app.logic import fibonacci

queue = None
worker_started = False


async def init_worker():
    global queue, worker_started
    if queue is None:
        queue = asyncio.Queue()
    if not worker_started:
        asyncio.create_task(worker_loop())
        worker_started = True


async def worker_loop():
    while True:
        n, future = await queue.get()
        result = fibonacci(n)
        future.set_result(result)


async def fib_worker(n: int) -> int:
    global queue, worker_started
    if queue is None or not worker_started:
        await init_worker()
    future = asyncio.get_event_loop().create_future()
    await queue.put((n, future))
    return await future
