FROM python:3.11-slim

WORKDIR /app
COPY ./db/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./db .

CMD ["python", "-u", "src/main.py"]