FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir boto3 botocore

COPY server.py .

CMD ["python3", "server.py"]

