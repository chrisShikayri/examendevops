# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instalar deps del sistema necesarios
RUN apt-get update && apt-get install -y build-essential gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Entrenar el modelo en build (o usar modelo ya existente)
RUN python model/train.py

ENV MODEL_PATH=/app/model/model.pkl
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
EXPOSE 80

CMD ["flask", "run", "--host=0.0.0.0", "--port=80"]
