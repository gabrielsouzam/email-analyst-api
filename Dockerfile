FROM python:3.11-slim

COPY --from=ghcr.io/astral-sh/uv:0.5.20 /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml .

# Instala dependências
RUN uv pip install --system --no-cache-dir -r pyproject.toml

COPY ./src .

EXPOSE 5000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]