This project is a Python-based FastAPI microservice that performs the following mathematical operations:
- Power calculation 
- Fibonacci number
- Factorial

Features:
- **FastAPI** RESTful API
- **Pydantic** for input validation & schema enforcement
- **SQLite** database for storing requests
- **In-memory caching** for Fibonacci
- **Async worker queue** for non-blocking execution
- **Logging middleware** for incoming/outgoing requests
- **Dockerized** and easy to run with Docker Compose
- **Cleaned** with flake8 and black
- **Testable** with pytest

Requirements:
- Python 3.10+
- Docker & Docker Compose (optional)

How to run:
1) pip install -r requirements.txt
2)
To run the app locally: uvicorn app.main:app --reload --app-dir src
then visit http://localhost:8000/docs

To run the app from docker: docker run -p 8000:8000 -v ${PWD}\math.db:/app/math.db math-api
then visit http://localhost:8000/docs
3) stop app: ctrl+C
4) see logs: sqlite-utils rows math.db request_log
5)  run tests: pytest