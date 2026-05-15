# syntax=docker/dockerfile:1

FROM python:3.11-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    FLASK_ENV=production \
    MODEL_PATH=/app/models/skin_rf.joblib

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libgl1 \
        libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt setup.py README.md ./
COPY src ./src
COPY ml ./ml
COPY frontend ./frontend
COPY app.py ./app.py

RUN python -m pip install --upgrade pip \
    && pip install -r requirements.txt \
    && pip install .

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5000/api/v1/health', timeout=3).read()"

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "120", "app:app"]
