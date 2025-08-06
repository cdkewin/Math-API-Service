from fastapi import FastAPI
from fastapi import Request
from app import database, schemas, logic, cache, workers
from app.logging_config import setup_logging


app = FastAPI() # Creates instance of FastAPI web server -> will be used by uvicorn

database.init_db()    # Initializes the database connection
cache.init_cache()     # Initializes the cache store


@app.on_event("startup")
async def startup_event():
    await workers.init_worker()


@app.post("/pow")
async def pow_api(req: schemas.PowerRequest):
    cached = cache.check_cache("pow", (req.base, req.exponent))
    if cached:
        return {"result": cached}
    result = logic.power(req.base, req.exponent)
    await database.save_to_db("pow", req.model_dump(), result)
    cache.set_cache("pow", (req.base, req.exponent), result)
    return {"result": result}


@app.post("/factorial")
async def fact_api(req: schemas.SingleInput):
    cached = cache.check_cache("factorial", req.number)
    if cached:
        return {"result": cached}
    result = logic.factorial(req.number)
    await database.save_to_db("factorial", req.model_dump(), result)
    cache.set_cache("factorial", req.number, result)
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
