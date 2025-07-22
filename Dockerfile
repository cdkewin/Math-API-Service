# 1. Base Python image
FROM python:3.10-slim

# 2. Working directory inside the container
WORKDIR /app

# 3. Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy project files
COPY . .

# 5. Expose port FastAPI will use
EXPOSE 8000

# 6. Command to run the API server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--app-dir", "src"]