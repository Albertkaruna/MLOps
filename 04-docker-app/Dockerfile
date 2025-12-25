FROM python:3.12-slim

WORKDIR /app

RUN apt update -y && apt install curl -y
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 3000

CMD ["python", "app.py"]