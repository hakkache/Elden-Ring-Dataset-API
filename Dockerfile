FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY data ./data

ENV DATA_DIR=/app/data
ENV SECRET_KEY=CHANGE_THIS_SECRET

# Railway compatibility - provide default PORT
CMD exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}