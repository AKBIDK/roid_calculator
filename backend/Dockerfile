# Multi-stage build para segurança e redução de superfície de ataque
FROM python:3.11-slim as builder

WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.11-slim as runner

# Criação de usuário não-privilegiado (Hefesto & Têmis Security Pattern)
RUN groupadd -g 10001 appuser &&     useradd -u 10001 -g appuser -s /bin/sh -m appuser

WORKDIR /app
COPY --from=builder /root/.local /home/appuser/.local
COPY . /app

RUN chown -R appuser:appuser /app
ENV PATH=/home/appuser/.local/bin:$PATH
USER appuser

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
