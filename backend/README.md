## testStructure

Small **FastAPI + SQLAlchemy (SQLite)** learning project used to practice:

- **Creating objects/models** (SQLAlchemy ORM)
- **Schemas** (Pydantic request bodies)
- **Database session handling**
- **Routes / routers** (auth + subscriptions)

The app auto-creates the database tables on startup.

## Tech stack

- **FastAPI**
- **SQLAlchemy** (SQLite)
- **JWT auth** with `python-jose`
- **Password hashing** with `passlib` + `bcrypt`
- **Settings via `.env`** using `pydantic-settings`

## Project structure

- `main.py`: FastAPI app + router registration + `Base.metadata.create_all(...)`
- `app/core/config.py`: settings loaded from `.env`
- `app/core/database.py`: SQLAlchemy engine + session dependency (`get_db`)
- `app/core/security.py`: password hashing + JWT creation
- `app/api/auth.py`: signup/signin routes
- `app/api/subscription.py`: subscription routes
- `app/models/`: SQLAlchemy models (`User`, `Subscription`)
- `app/schemas/`: Pydantic schemas (request bodies)

## Setup

### 1) Create `.env`

This project requires environment variables (the app will fail to start without them). Create a file named `.env` in the project root:

```env
PROJECT_NAME=testStructure
VERSION=0.1.0

# SQLite database (file in project root)
DATABASE_URL=sqlite:///./subscription.db

# Not used yet, but required by Settings
FRONTEND_URL=http://localhost:3000

# JWT config
SECRET_KEY=change-me-to-a-long-random-secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### 2) Install dependencies

This repo includes a `uv.lock`, so the easiest path is using **uv**:

```bash
uv sync
```

If you are not using `uv`, install the common runtime deps manually (example):

```bash
pip install fastapi uvicorn sqlalchemy pydantic-settings "python-jose[cryptography]" "passlib[bcrypt]"
```

## Run the API

Using **uv**:

```bash
uv run uvicorn main:app --reload
```

Without uv:

```bash
uvicorn main:app --reload
```

Then open:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Routes (current)

### Health

- `GET /` → `{"message": "API is running"}`

### Auth (`/api/auth`)

- `POST /api/auth/signup`
  - Body (JSON): `{ "username": "...", "email": "...", "password": "..." }`
  - Creates the user + a default subscription row.
- `POST /api/auth/signin`
  - Form data (OAuth2 password flow): `username=...&password=...`
  - Returns `{ access_token, token_type, user_id }`
- `GET /api/auth/users`
  - Returns all users (raw SQLAlchemy objects).

### Subscriptions (`/api/subscriptions`)

- `GET /api/subscriptions/`
  - Returns all subscriptions (raw SQLAlchemy objects).

## Quick test with curl

### Signup

```bash
curl -X POST "http://127.0.0.1:8000/api/auth/signup" ^
  -H "Content-Type: application/json" ^
  -d "{\"username\":\"test\",\"email\":\"test@example.com\",\"password\":\"secret\"}"
```

### Signin (OAuth2 form)

```bash
curl -X POST "http://127.0.0.1:8000/api/auth/signin" ^
  -H "Content-Type: application/x-www-form-urlencoded" ^
  -d "username=test@example.com&password=secret"
```

### List subscriptions

```bash
curl "http://127.0.0.1:8000/api/subscriptions/"
```

## Notes / WIP

- This is a **learning / test project** (some pieces are intentionally minimal).
- If you want, I can also help you:
  - add a proper `pyproject.toml` dependency list,
  - return Pydantic response models instead of raw SQLAlchemy objects,
  - protect routes with `get_current_user`.
