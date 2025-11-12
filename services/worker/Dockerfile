FROM python:3.14-slim


RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl ca-certificates tzdata git \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
EXPOSE 8081
CMD ["python", "-m", "app.run_worker"]