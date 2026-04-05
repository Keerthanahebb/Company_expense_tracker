FROM python:3.10-slim

WORKDIR /app

# Copy only required files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Environment
ENV PYTHONUNBUFFERED=1

# Run FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]