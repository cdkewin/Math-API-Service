def power(base: float, exponent: float) -> float:
    return base**exponent


def factorial(n: int) -> int:
    if n == 0:
        return 1
    return n * factorial(n - 1)


def fibonacci(n: int) -> int:
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a
