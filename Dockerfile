FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip  install -r requirements.txt

COPY . .

RUN flask db stamp head

CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 flaskr:app