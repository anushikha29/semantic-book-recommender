#Stage 1
FROM python:3.10 as builder

WORKDIR /app

RUN pip install --upgrade pip build

COPY requirements.txt .

RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt


# Stage 2: The final, slim stage
FROM python:3.10-slim

WORKDIR /app

COPY --from=builder /wheels /wheels

RUN pip install --no-cache-dir /wheels/*

COPY --from=builder /usr/local/bin/ /usr/local/bin/

COPY . .

CMD ["streamlit", "run", "app.py"]