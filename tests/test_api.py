from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_pow():
    response = client.post("/pow", json={"base": 2, "exponent": 5})
    assert response.status_code == 200
    assert response.json() == {"result": 32.0}


def test_fib():
    response = client.post("/fib", json={"number": 10})
    assert response.status_code == 200
    assert response.json()["result"] == 55  # 10th Fibonacci number


def test_factorial():
    response = client.post("/factorial", json={"number": 5})
    assert response.status_code == 200
    assert response.json()["result"] == 120


def test_invalid_input_pow():
    response = client.post("/pow", json={"base": "abc", "exponent": 2})
    assert response.status_code == 422  # Unprocessable Entity


def test_invalid_input_fib():
    response = client.post("/fib", json={"number": -5})
    assert response.status_code == 422
