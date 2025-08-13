from fastapi import FastAPI
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from app import database, schemas, logic, cache, workers
from app.logging_config import setup_logging
from fastapi import HTTPException
from pydantic import BaseModel


app = FastAPI()  # Creates instance of FastAPI web server -> will be used by uvicorn

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

database.init_db()  # Initializes the database connection
cache.init_cache()  # Initializes the cache store


@app.on_event("startup")
async def startup_event():
    await workers.init_worker()


@app.post("/pow")
async def pow_api(req: schemas.PowerRequest):
    cached = cache.check_cache("pow", (req.base, req.exponent))
    database.save_to_db("pow", req.model_dump(), cached if cached else logic.power(req.base, req.exponent))
    if cached:
        return {"result": cached}
    result = logic.power(req.base, req.exponent)
    cache.set_cache("pow", (req.base, req.exponent), result)
    return {"result": result}


@app.post("/factorial")
async def fact_api(req: schemas.SingleInput):
    cached = cache.check_cache("factorial", req.number)
    database.save_to_db("factorial", req.model_dump(), cached if cached else logic.factorial(req.number))
    if cached:
        return {"result": cached}
    result = logic.factorial(req.number)
    cache.set_cache("factorial", req.number, result)
    return {"result": result}


@app.post("/fib")
async def fib_api(req: schemas.SingleInput):
    cached = cache.check_cache("fib", req.number)
    database.save_to_db("fib", req.model_dump(), cached if cached else await workers.fib_worker(req.number))
    if cached:
        return {"result": cached}
    result = await workers.fib_worker(req.number)
    cache.set_cache("fib", req.number, result)
    return {"result": result}


class UserCreate(BaseModel):
    username: str
    password: str


@app.post("/register")
def register(user: UserCreate):
    if database.get_user(user.username):
        raise HTTPException(status_code=400, detail="Username already exists")
    database.create_user(user.username, user.password)
    return {"message": "User registered successfully"}


@app.post("/login")
def login(user: UserCreate):
    db_user = database.get_user(user.username)
    if not db_user or not database.verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"token": f"dummy-token-for-{user.username}"}


setup_logging()


@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"Incoming request: {request.method} {request.url.path}")
    response = await call_next(request)
    print(f"Response status: {response.status_code}")
    return response


@app.get("/cache")
def get_cache():
    from app import cache

    return cache.cache_store
