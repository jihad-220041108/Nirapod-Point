# ⚙️ NirapodPoint — Backend Setup Guide

**FastAPI · Python 3.11+ · PostgreSQL + PostGIS · Redis · YOLOv9c · MediaPipe · CLIP**

---

## 📋 Table of Contents

- [Prerequisites](#-prerequisites)
- [Quick Start (Docker)](#-quick-start-with-docker-recommended)
- [Manual Setup (Step-by-Step)](#-manual-setup-step-by-step)
- [Environment Variables Reference](#-environment-variables-reference)
- [Database Setup](#-database-setup)
- [AI Model Setup](#-ai-model-setup)
- [Running the Server](#-running-the-server)
- [Running Tests](#-running-tests)
- [Project Structure](#-project-structure)
- [API Reference](#-api-reference)
- [Troubleshooting](#-troubleshooting)

---

## ✅ Prerequisites

Before you begin, make sure the following are installed on your machine:

| Tool | Version | Download |
|---|---|---|
| Python | 3.11+ | https://python.org/downloads |
| PostgreSQL | 16+ | https://postgresql.org/download |
| PostGIS | 3.x | Bundled with PostgreSQL installers |
| Redis | 7+ | https://redis.io/download |
| Docker Desktop | Latest | https://docker.com/products/docker-desktop *(optional)* |
| Git | Latest | https://git-scm.com |

> **Windows Users:** Redis does not have an official Windows build. Use either **Docker** (recommended) or **WSL 2** to run Redis on Windows.

---

## 🐳 Quick Start with Docker (Recommended)

This is the easiest method. Docker handles PostgreSQL, Redis, and the API server automatically.

### Step 1 — Clone the repository

```bash
git clone https://github.com/ArafatBytes/Nirapod-Point-Mobile-App.git
cd "NirapodPoint App/backend"
```

### Step 2 — Create the environment file

```bash
# Windows (PowerShell)
Copy-Item .env.example .env

# Linux / Mac
cp .env.example .env
```

Open `.env` in any text editor and fill in at minimum:
- `POSTGRES_PASSWORD` — choose any password
- `JWT_SECRET_KEY` — generate a 32+ char random string
- `SECRET_KEY` — generate another 32+ char random string

### Step 3 — Download the YOLOv9c AI model

```bash
# Make sure you are in the backend/ directory
python scripts/download_models.py
```

This downloads `yolov9c.pt` (~82 MB) into the `backend/` directory.

### Step 4 — Start all services

```bash
docker-compose up -d
```

Docker Compose starts:
- **PostgreSQL + PostGIS** on port `5432`
- **Redis** on port `6379`
- **FastAPI API** on port `8000`
- **Celery Worker** (background tasks)

### Step 5 — Apply database migrations

```bash
docker-compose exec api alembic upgrade head
```

### Step 6 — Verify it's running

```bash
# Check all containers are healthy
docker-compose ps

# Hit the health endpoint
curl http://localhost:8000/health
# Expected: {"status": "healthy", ...}
```

**API is live at:** `http://localhost:8000`
**Swagger docs:** `http://localhost:8000/docs`
**ReDoc:** `http://localhost:8000/redoc`

---

## 🛠️ Manual Setup (Step-by-Step)

Use this if you prefer to run without Docker or want a development environment.

---

### STEP 1 — Clone & Navigate

```bash
git clone https://github.com/ArafatBytes/Nirapod-Point-Mobile-App.git
cd "NirapodPoint App/backend"
```

---

### STEP 2 — Create a Python Virtual Environment

```powershell
# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1
```

```bash
# Linux / Mac
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` at the start of your terminal prompt.

> ⚠️ **Always activate the virtual environment before running any commands.**

---

### STEP 3 — Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This installs ~50+ packages including FastAPI, SQLAlchemy, PyTorch, YOLOv9c, MediaPipe, and all other dependencies. This may take **5–15 minutes** depending on your connection speed.

> 💡 **Tip:** If PyTorch installation fails, visit https://pytorch.org/get-started to get the correct command for your OS and CUDA version.

---

### STEP 4 — Install & Configure PostgreSQL with PostGIS

#### 4a — Install PostgreSQL

Download and install PostgreSQL 16 from: https://postgresql.org/download

During installation:
- Set a password for the `postgres` superuser
- Keep the default port `5432`
- Make sure to select **"Stack Builder"** — use it to install **PostGIS**

#### 4b — Create the database

Open **pgAdmin** or **psql**:

```sql
-- Connect as postgres superuser
CREATE USER nirapodpoint_user WITH PASSWORD 'your-secure-password';
CREATE DATABASE nirapodpoint_db OWNER nirapodpoint_user;
\c nirapodpoint_db
CREATE EXTENSION postgis;
CREATE EXTENSION postgis_topology;
```

Or using the command line:

```bash
psql -U postgres -c "CREATE USER nirapodpoint_user WITH PASSWORD 'yourpassword';"
psql -U postgres -c "CREATE DATABASE nirapodpoint_db OWNER nirapodpoint_user;"
psql -U postgres -d nirapodpoint_db -c "CREATE EXTENSION postgis;"
psql -U postgres -d nirapodpoint_db -c "CREATE EXTENSION postgis_topology;"
```

---

### STEP 5 — Install & Start Redis

**Windows (via Docker — easiest):**
```powershell
docker run -d -p 6379:6379 --name nirapod-redis redis:7-alpine
```

**Linux:**
```bash
sudo apt-get update && sudo apt-get install -y redis-server
sudo systemctl start redis-server
sudo systemctl enable redis-server
```

**Mac:**
```bash
brew install redis
brew services start redis
```

Verify Redis is running:
```bash
redis-cli ping
# Expected output: PONG
```

---

### STEP 6 — Configure Environment Variables

```bash
# Windows (PowerShell)
Copy-Item .env.example .env

# Linux / Mac
cp .env.example .env
```

Open `.env` and fill in the required values:

```env
# ── REQUIRED ─────────────────────────────────────────────────
SECRET_KEY=change-this-to-a-random-64-char-string
JWT_SECRET_KEY=change-this-to-another-random-64-char-string

# Database (match what you created in Step 4)
POSTGRES_USER=nirapodpoint_user
POSTGRES_PASSWORD=your-secure-password
POSTGRES_DB=nirapodpoint_db
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
DATABASE_URL=postgresql+asyncpg://nirapodpoint_user:your-secure-password@localhost:5432/nirapodpoint_db

# Redis (match what you set up in Step 5)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_URL=redis://localhost:6379/0

# ── OPTIONAL (features degrade gracefully if not set) ────────
# SMS via CloudWaveBD
CLOUDWAVEBD_API_KEY=your-api-key

# Firebase push notifications
FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json
FIREBASE_PROJECT_ID=your-project-id

# Supabase file storage
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=your-anon-key

# Email for SOS alerts
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-gmail-app-password
```

> 💡 **Generate secure keys:**
> ```python
> python -c "import secrets; print(secrets.token_hex(32))"
> ```

---

### STEP 7 — Download AI Models

```bash
# Make sure venv is activated and you're in backend/
python scripts/download_models.py
```

This downloads `yolov9c.pt` to `backend/yolov9c.pt` (~82 MB).

**MediaPipe** and **CLIP** models are downloaded automatically the first time the server starts (cached in `~/.cache/`).

---

### STEP 8 — Run Database Migrations

```bash
# Make sure venv is activated
alembic upgrade head
```

Expected output:
```
INFO  [alembic.runtime.migration] Running upgrade  -> abc123, initial schema
INFO  [alembic.runtime.migration] Running upgrade abc123 -> def456, add postgis columns
...
```

---

### STEP 9 — Start the API Server

Open **Terminal 1:**
```bash
# Activate venv first!
# Windows: .\venv\Scripts\Activate.ps1
# Linux/Mac: source venv/bin/activate

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Expected output:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

Open **Terminal 2** (for background task processing):
```bash
source venv/bin/activate   # or .\venv\Scripts\Activate.ps1

celery -A app.core.celery_app worker --loglevel=info
```

---

### STEP 10 — Verify Everything Works

```bash
# Health check
curl http://localhost:8000/health

# Open Swagger UI in browser
start http://localhost:8000/docs     # Windows
open  http://localhost:8000/docs     # Mac
xdg-open http://localhost:8000/docs  # Linux
```

You should see the interactive Swagger API documentation.

---

## 🔑 Environment Variables Reference

| Variable | Required | Default | Description |
|---|---|---|---|
| `SECRET_KEY` | ✅ | — | App secret key (min 32 chars) |
| `JWT_SECRET_KEY` | ✅ | — | JWT signing key |
| `DATABASE_URL` | ✅ | — | Full async PostgreSQL URL |
| `REDIS_URL` | ✅ | — | Redis connection URL |
| `DEBUG` | ❌ | `True` | Enable debug mode |
| `JWT_ALGORITHM` | ❌ | `HS256` | JWT algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | ❌ | `1440` | Token expiry (24h) |
| `CLOUDWAVEBD_API_KEY` | ❌ | — | SMS gateway key |
| `FIREBASE_CREDENTIALS_PATH` | ❌ | — | Path to FCM JSON |
| `SMTP_HOST` | ❌ | — | Email SMTP server |
| `SMTP_USER` | ❌ | — | Email sender address |
| `SMTP_PASSWORD` | ❌ | — | Email app password |
| `SUPABASE_URL` | ❌ | — | Supabase project URL |
| `SUPABASE_KEY` | ❌ | — | Supabase anon key |
| `OSRM_BASE_URL` | ❌ | `http://router.project-osrm.org` | OSRM routing server |
| `SOS_VIDEO_MAX_DURATION` | ❌ | `300` | Max SOS video seconds |
| `DANGER_ZONE_THRESHOLD` | ❌ | `75` | Crime score alert threshold |
| `LOCATION_UPDATE_INTERVAL` | ❌ | `60` | GPS update interval (sec) |

---

## 🗄️ Database Setup

### Apply migrations

```bash
alembic upgrade head
```

### Create a new migration (after model changes)

```bash
alembic revision --autogenerate -m "describe your change"
alembic upgrade head
```

### Rollback one migration

```bash
alembic downgrade -1
```

### Check migration history

```bash
alembic history --verbose
alembic current
```

---

## 🤖 AI Model Setup

| Model | Size | How to get |
|---|---|---|
| **YOLOv9c** (`yolov9c.pt`) | ~82 MB | `python scripts/download_models.py` |
| **MediaPipe Pose** | ~30 MB | Auto-downloaded on first use |
| **CLIP** (`openai/clip-vit-base-patch32`) | ~600 MB | Auto-downloaded on first use via HuggingFace |

All auto-downloaded models are cached in:
- Windows: `C:\Users\<you>\.cache\huggingface\`
- Linux/Mac: `~/.cache/huggingface/`

---

## 🏃 Running the Server

### Development (with auto-reload)

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production

```bash
uvicorn app.main:app --workers 4 --host 0.0.0.0 --port 8000
```

### With Gunicorn (production-grade)

```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

---

## 🧪 Running Tests

```bash
# Activate venv first
source venv/bin/activate  # or .\venv\Scripts\Activate.ps1

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=app tests/ --cov-report=term-missing

# Run a specific test file
pytest tests/test_crime_vision.py -v

# Run a specific test function
pytest tests/test_crime_vision.py::TestCrimeVisionService::test_model_loading -v
```

Expected output:
```
========================= test session starts ==========================
tests/test_crime_vision.py::TestCrimeVisionService::test_service_initialization PASSED
tests/test_crime_vision.py::TestCrimeVisionService::test_model_loading PASSED
...
========================= 29 passed in 16.83s ==========================
```

---

## 📂 Project Structure

```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── auth.py          # POST /register, /login
│   │       │   ├── crimes.py        # Crime CRUD + AI analysis
│   │       │   ├── routes.py        # Safe route calculation
│   │       │   ├── tracking.py      # GPS location updates
│   │       │   ├── sos.py           # SOS emergency trigger
│   │       │   └── users.py         # Profile + contacts
│   │       └── api.py               # Router aggregation
│   ├── core/
│   │   ├── config.py                # Pydantic Settings (reads .env)
│   │   ├── database.py              # Async SQLAlchemy engine + session
│   │   ├── security.py              # JWT create/verify, bcrypt
│   │   ├── celery_app.py            # Celery + Redis broker
│   │   └── redis.py                 # Redis client singleton
│   ├── models/                      # SQLAlchemy ORM models
│   │   ├── user.py                  # User, EmergencyContact
│   │   ├── crime.py                 # CrimeReport
│   │   ├── sos.py                   # SOSEvent
│   │   ├── location.py              # LocationHistory
│   │   └── police.py                # PoliceStation
│   ├── schemas/                     # Pydantic request/response models
│   │   ├── auth.py
│   │   ├── crime.py
│   │   ├── route.py
│   │   └── user.py
│   ├── services/                    # Business logic layer
│   │   ├── ai/
│   │   │   └── crime_vision_service.py   # ML Fusion Engine
│   │   ├── route_service.py         # OSRM + safety scoring
│   │   ├── sos_service.py           # SOS orchestration
│   │   ├── email_service.py         # SMTP email sending
│   │   └── sms_service.py           # CloudWaveBD SMS
│   ├── utils/
│   │   ├── geospatial.py            # Distance, bounding box
│   │   └── notifications.py         # FCM push notifications
│   └── main.py                      # FastAPI app entry point
│
├── alembic/                         # Database migration scripts
│   ├── versions/                    # Migration files (auto-generated)
│   └── env.py                       # Alembic environment config
│
├── tests/
│   └── test_crime_vision.py         # AI service unit tests (29 cases)
│
├── scripts/
│   └── download_models.py           # YOLOv9c model downloader
│
├── requirements.txt                 # Python package list
├── Dockerfile                       # Container definition
├── docker-compose.yml               # Multi-service orchestration
├── .env.example                     # Environment variable template
└── yolov9c.pt                       # YOLOv9c weights (not in git)
```

---

## 📡 API Reference

### Authentication

| Method | Endpoint | Body | Response |
|---|---|---|---|
| `POST` | `/api/v1/auth/register` | `{email, password, full_name}` | `201` user object |
| `POST` | `/api/v1/auth/login` | `{email, password}` | `200` `{access_token}` |
| `GET` | `/api/v1/auth/me` | — (Bearer token) | `200` current user |

### Crime Reports

| Method | Endpoint | Notes |
|---|---|---|
| `POST` | `/api/v1/crimes/` | Multipart: fields + optional image |
| `GET` | `/api/v1/crimes/` | List own reports |
| `GET` | `/api/v1/crimes/nearby` | Query params: `lat`, `lon`, `radius_km` |
| `POST` | `/api/v1/crimes/{id}/analyze` | Trigger AI analysis on existing report |

### Routes

| Method | Endpoint | Notes |
|---|---|---|
| `POST` | `/api/v1/routes/calculate` | Body: `{origin, destination}` → 3 routes |

### SOS

| Method | Endpoint | Notes |
|---|---|---|
| `POST` | `/api/v1/sos/trigger` | Multipart: location JSON + optional video |
| `GET` | `/api/v1/sos/nearest-police` | Query: `lat`, `lon`, `radius_km` |

### User

| Method | Endpoint | Notes |
|---|---|---|
| `GET` | `/api/v1/users/me` | Get profile |
| `PUT` | `/api/v1/users/emergency-contacts` | Update contacts list |

### Health

| Method | Endpoint |
|---|---|
| `GET` | `/health` |

**Full interactive docs:** http://localhost:8000/docs

---

## 🔍 Troubleshooting

### ❌ `ModuleNotFoundError` when running uvicorn

**Cause:** Virtual environment not activated.

```bash
# Windows
.\venv\Scripts\Activate.ps1

# Linux/Mac
source venv/bin/activate
```

---

### ❌ `asyncpg.exceptions.InvalidCatalogNameError: database does not exist`

**Cause:** Database not created yet.

```bash
psql -U postgres -c "CREATE DATABASE nirapodpoint_db;"
psql -U postgres -d nirapodpoint_db -c "CREATE EXTENSION postgis;"
```

---

### ❌ `redis.exceptions.ConnectionError`

**Cause:** Redis is not running.

```bash
# Windows — run Redis in Docker
docker run -d -p 6379:6379 --name redis redis:7-alpine

# Linux
sudo systemctl start redis-server

# Verify
redis-cli ping   # should print: PONG
```

---

### ❌ `yolov9c.pt not found`

```bash
python scripts/download_models.py
```

Or manually download from: https://github.com/WongKinYiu/yolov9/releases and place `yolov9c.pt` in the `backend/` directory.

---

### ❌ `alembic: command not found`

**Cause:** Alembic not installed or venv not activated.

```bash
pip install alembic
alembic upgrade head
```

---

### ❌ PostGIS extension error

```sql
-- Run as postgres superuser in psql
\c nirapodpoint_db
CREATE EXTENSION IF NOT EXISTS postgis;
```

---

### ❌ Port 8000 already in use

```bash
# Windows — find and kill the process
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill
```

---

## 📦 Production Deployment Checklist

- [ ] Set `DEBUG=False` in `.env`
- [ ] Use strong `SECRET_KEY` and `JWT_SECRET_KEY`
- [ ] Configure production PostgreSQL with SSL
- [ ] Use production Redis with password
- [ ] Enable HTTPS (via Nginx + Let's Encrypt or AWS ALB)
- [ ] Set proper `ALLOWED_ORIGINS` in CORS config
- [ ] Configure Sentry for error monitoring
- [ ] Set up database backup schedule
- [ ] Enable rate limiting on sensitive endpoints

---

*NirapodPoint Backend — Islamic University of Technology, CSE 4510*
