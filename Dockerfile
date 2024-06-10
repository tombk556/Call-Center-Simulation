FROM python:3.9.2-slim

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY src/ /app/src/
COPY static/ /app/static/
COPY templates/ /app/templates/
COPY app.py /app/

EXPOSE 3000