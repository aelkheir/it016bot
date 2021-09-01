FROM python:3.9-slim

WORKDIR /app

ARG FLASK_APP=flaskr

ARG SQLALCHEMY_DATABASE_URI=postgresql://ngjhycxpfirzwk:579f25b1d29f0db6bd5eaf10f0966c3cd135f5a5eaa8d41749c4223998670a86@ec2-52-203-74-38.compute-1.amazonaws.com:5432/derqs0k29i4qan

COPY requirements.txt .

RUN pip  install -r requirements.txt

COPY . .

RUN flask db stamp head

CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 flaskr:app