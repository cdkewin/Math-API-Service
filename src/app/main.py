from fastapi import FastAPI
from fastapi import Request
from app import database, schemas, logic, cache, workers
from app.logging_config import setup_logging
from pydantic import BaseModel, Field
import asyncio

app = FastAPI()

database.init_db()
cache.init_cache()

@app.on_event("startup")
async def startup_event():
    await workers.init_worker()


@app.post("/pow")
async def pow_api(req: schemas.PowerRequest):
    result = logic.power(req.base, req.exponent)
    await database.save_to_db("pow", req.model_dump(), result)
    return {"result": result}


@app.post("/factorial")
async def fact_api(req: schemas.SingleInput):
    result = logic.factorial(req.number)
    await database.save_to_db("factorial", req.model_dump(), result)
    return {"result": result}


@app.post("/fib")
async def fib_api(req: schemas.SingleInput):
    cached = cache.check_cache("fib", req.number)
    if cached:
        return {"result": cached}

    result = await workers.fib_worker(req.number)
    cache.set_cache("fib", req.number, result)
    await database.save_to_db("fib", req.model_dump(), result)
    return {"result": result}


setup_logging()


@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"Incoming request: {request.method} {request.url.path}")
    response = await call_next(request)
    print(f"Response status: {response.status_code}")
    return response
