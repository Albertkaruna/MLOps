FROM python:3.12-slim

WORKDIR /app

RUN apt-get update -y && apt-get install -y curl

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install torch==2.9.0 --index-url https://download.pytorch.org/whl/cpu

COPY . .

ENV HF_HOME=hf_cache

EXPOSE 5000

CMD ["python", "app.py"]