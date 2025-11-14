## Stage 1: Build
FROM python:3.11-slim AS build

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

## Stage 2: Runtime
FROM python:3.11-slim
WORKDIR /app

COPY --from=build /usr/local /usr/local
COPY app.py .

ENV APP_NAME="DevOps Python App"
ENV APP_VERSION="1.0.0"
ENV ENVIRONMENT="development"
ENV PORT=5000

EXPOSE 5000

CMD ["python", "app.py"]
