FROM python:3.12-slim

RUN apt-get update -y && apt-get install -y curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# RUN adduser --disabled-password --gecos '' appuser
# USER appuser

WORKDIR /app
# RUN chown -R appuser:appuser /app

ENV HF_HOME=/app/model_cache
ARG APP_VERSION=1.0.0
LABEL owner="Karuna" version="${APP_VERSION}"

COPY requirements.txt .

# Use BuildKit cache mount for pip downloads
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install torch==2.5.1 --index-url https://download.pytorch.org/whl/cpu

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

COPY . .

EXPOSE 5000
HEALTHCHECK --interval=30s --timeout=300s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1
    
CMD ["python", "app.py"]