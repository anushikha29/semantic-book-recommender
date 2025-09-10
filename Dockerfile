# Stage 1
FROM python:3.10 as builder

WORKDIR /app

RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt


# Stage 2
FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

COPY --from=builder /wheels /wheels

RUN pip install --no-cache-dir /wheels/*

RUN pip install --no-cache-dir torch --extra-index-url https://download.pytorch.org/whl/cpu

COPY . .

CMD ["streamlit", "run", "app.py"]