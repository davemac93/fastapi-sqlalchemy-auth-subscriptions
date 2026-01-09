# --- Stage 1: Build ---
FROM python:3.12-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY requirements.txt .

RUN uv pip install --system --no-cache -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# --- Stage 2: Runtime ---
FROM python:3.12-slim

# 1. Grab 'uv' from the official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
    
# 2. Set the work directory
WORKDIR /app
    
# 3. Copy dependencies first
COPY requirements.txt .
    
# 4. Install dependencies using uv sync logic
# We use --system to install into the global site-packages of the container
RUN uv pip install --system --no-cache -r requirements.txt
    
# 5. Copy your application
COPY . .
    
# 6. Use 'python -m uvicorn' to start the app
# This is a safer way to call uvicorn because it doesn't rely on the $PATH
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]