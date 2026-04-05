FROM python:3.12-slim

# system deps (for psycopg2)
RUN apt-get update && apt-get install -y libpq-dev gcc

WORKDIR /app

# copy requirements first
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# copy project
COPY . .

# expose port
EXPOSE 8000

# run app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
