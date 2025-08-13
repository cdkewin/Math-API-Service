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
2)To run the app locally: uvicorn app.main:app --reload --app-dir src --host 127.0.0.1 --port 8080   
then visit "WebPage.html" from the project directory or http://localhost:8080/docs
To run the app from docker: docker-compose up --build
then visit http://localhost:8080/docs
3) stop app: ctrl+C
4) see logs: sqlite-utils rows math.db request_log
5) run tests: pytest -v
