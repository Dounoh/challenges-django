FROM python:3.13-slim
ENV PYTHONDONTWRITEBYCODE = 1
ENV PYTHONBUFFERED = 1

WORKDIR /app
COPY requirements.txt .

RUN pip install upgrade pip && install -r requirements.txt

COPY . .
EXPOSE 8080

CMD ['uvicorn', 'conf.asgi:application', '--host', '0.0.0.', '--port', '8080']
