# 🛡️ NirapodPoint — Smart Safety Navigation System

> **"Your Safety, Our Priority"**

[![React Native](https://img.shields.io/badge/React_Native-0.81.5-61DAFB?logo=react)](https://reactnative.dev/)
[![Expo](https://img.shields.io/badge/Expo-SDK_54-000020?logo=expo)](https://expo.dev/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python)](https://python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16_+_PostGIS-336791?logo=postgresql)](https://postgis.net/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Architecture](#️-architecture)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [AI Pipeline](#-ai-pipeline)
- [API Reference](#-api-reference)
- [Testing](#-testing)
- [Performance Targets](#-performance-targets)
- [Roadmap](#-development-roadmap)
- [Team](#-team)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

**NirapodPoint** (নিরাপদ পয়েন্ট — Bengali for *"Safe Point"*) is a comprehensive cross-platform mobile safety navigation application. It addresses the critical gap left by traditional navigation apps like Google Maps, which focus solely on speed and distance without considering the **safety** of a route.

NirapodPoint combines **real-time community crime data**, **multi-model AI image analysis**, **geospatial safety scoring**, and **emergency response** into a single unified platform for Android and iOS.

### Why NirapodPoint?

| Traditional Navigation | NirapodPoint |
|---|---|
| Fastest route only | Fastest + **Safest** route |
| No crime awareness | Real-time crime heatmaps |
| Manual emergency calls | Voice-activated SOS + auto-recording |
| No community reporting | AI-verified community crime reports |
| No danger alerts | Geofence-based push notifications |

---

## ✨ Key Features

### 1. 🤖 AI-Powered Crime Detection (ML Fusion Engine)
- **YOLOv9c** object detection — weapons, persons, dangerous objects (40% weight)
- **MediaPipe** pose estimation — 8 action types, 3 threat levels (35% weight)
- **CLIP** scene classification — environmental context analysis (25% weight)
- Weighted voting with cross-model **confidence calibration**
- Auto-generated crime titles and descriptions
- Smart "No Crime Detected ✅" result for safe images

### 2. 📋 Community Crime Reporting
- Submit reports with category, severity, GPS location, and optional image
- AI analysis runs automatically on every attached photo
- Admin verification and moderation system
- Personal report history and status tracking
- Real-time crime heatmap visualization

### 3. 🗺️ Smart Route Planning
- Three ranked route options: **Optimal**, **Safest**, **Fastest**
- Per-route safety score (0–100) computed from live crime data
- Composite scoring: `0.3 × regional_risk + 0.7 × local_incident_risk`
- Road-network accuracy via **OSRM** engine
- Graceful fallback when OSRM is unavailable

### 4. 📍 Background GPS & Danger Zone Alerts
- Silent background tracking every 60 seconds (battery-optimised)
- Geofence detection triggers **Firebase FCM** push notifications
- Alternative route suggestions when entering danger zones

### 5. 🆘 SOS Emergency System
- **Voice-activated**: "NirapodPoint Emergency" (works screen-locked)
- Automatic camera recording (up to 5 minutes)
- Simultaneous alerts to:
  - All saved emergency contacts (email + video attachment)
  - Nearest police stations within 50 km (spatial query)
  - SMS via **CloudWaveBD** gateway
- Full incident logging to database

### 6. 👤 User Profile Management
- Emergency contact management (name, email, phone)
- Location history and SOS event log
- Secure JWT authentication, bcrypt password storage

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────────┐
│              📱 Mobile App (React Native / Expo)              │
│  ┌──────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐  │
│  │   Auth   │  │ Map+Route │  │ Crime AI  │  │   SOS     │  │
│  │  Module  │  │  Module   │  │  Report   │  │ Emergency │  │
│  └──────────┘  └───────────┘  └───────────┘  └───────────┘  │
└──────────────────────────┬───────────────────────────────────┘
                           │  HTTPS / REST  /api/v1
┌──────────────────────────▼───────────────────────────────────┐
│           ⚙️  Backend API (FastAPI / Python 3.11+)            │
│  ┌──────────────┐  ┌─────────────┐  ┌──────────────────────┐ │
│  │  ML Fusion   │  │   Route     │  │    SOS Service       │ │
│  │  Engine      │  │   Service   │  │    Auth / JWT        │ │
│  │  YOLOv9c     │  │   OSRM      │  │    Email / SMS       │ │
│  │  MediaPipe   │  │   Safety    │  │                      │ │
│  │  CLIP        │  │   Scoring   │  │                      │ │
│  └──────────────┘  └─────────────┘  └──────────────────────┘ │
└──────────────────────────┬───────────────────────────────────┘
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
   ┌─────────────┐  ┌──────────┐   ┌───────────────────────┐
   │ PostgreSQL  │  │  Redis   │   │   External Services   │
   │ + PostGIS   │  │  Cache   │   │  • Firebase FCM       │
   │             │  │          │   │  • CloudWaveBD SMS    │
   │  Spatial    │  │ Sessions │   │  • Supabase Storage   │
   │  Queries    │  │ Tokens   │   │  • OSRM Router        │
   └─────────────┘  └──────────┘   └───────────────────────┘
```

---

## 🔧 Technology Stack

### Frontend (Mobile App)

| Technology | Version | Purpose |
|---|---|---|
| React Native | 0.81.5 | Core mobile framework |
| Expo SDK | ~54.0.0 | Build toolchain & native APIs |
| TypeScript | 5.3.3 | Static typing |
| Zustand | 4.5.5 | Lightweight state management |
| React Navigation | 6.x | Screen navigation |
| react-native-maps | 1.20.1 | Map rendering |
| expo-location | ~19.0.8 | GPS & background tracking |
| expo-camera | ~17.0.10 | SOS video recording |
| @react-native-voice/voice | 3.2.4 | Voice activation |
| expo-notifications | 0.32.16 | FCM push notifications |
| @supabase/supabase-js | 2.86.2 | File storage & auth |
| @tanstack/react-query | 5.59.0 | Server state caching |
| axios | 1.7.9 | HTTP client |
| react-hook-form + yup | 7.53 / 1.4 | Form validation |
| lottie-react-native | 7.3.1 | Animations |

### Backend (API Server)

| Technology | Version | Purpose |
|---|---|---|
| FastAPI | 0.104+ | REST API framework |
| Python | 3.11+ | Core language |
| SQLAlchemy (async) | Latest | ORM |
| asyncpg | Latest | Async PostgreSQL driver |
| Alembic | Latest | Database migrations |
| GeoAlchemy2 | Latest | PostGIS spatial types |
| python-jose | Latest | JWT tokens |
| passlib[bcrypt] | Latest | Password hashing |
| Redis / aioredis | Latest | Cache layer |
| Celery | 5.3.6 | Background task queue |
| httpx | 0.26.0 | Async HTTP (OSRM calls) |
| ultralytics | 8.1.34 | YOLOv9c object detection |
| mediapipe | Latest | Pose estimation |
| transformers (HuggingFace) | Latest | CLIP scene classification |
| torch / torchvision | Latest | PyTorch inference |
| opencv-python | Latest | Image preprocessing |
| firebase-admin | 6.4.0 | FCM push notifications |
| geopy | 2.4.1 | Geodesic distance calculations |
| shapely | ≥2.0.7 | Geospatial geometry |

### Infrastructure & Services

| Technology | Role |
|---|---|
| Docker & Docker Compose | Containerisation |
| PostgreSQL 16 + PostGIS | Primary geospatial database |
| Redis 7 | Token cache & session store |
| Firebase Cloud Messaging | Mobile push notifications |
| Supabase | File storage & schema cache |
| CloudWaveBD | Primary SMS gateway (Bangladesh) |
| OSRM | Open-source road routing engine |
| GitHub Actions | CI/CD pipeline |

---

## 📂 Project Structure

```
NirapodPoint App/
├── backend/                          # FastAPI Python backend
│   ├── app/
│   │   ├── api/v1/endpoints/         # REST API route handlers
│   │   │   ├── auth.py               # JWT auth endpoints
│   │   │   ├── crimes.py             # Crime reporting
│   │   │   ├── routes.py             # Route calculation
│   │   │   ├── sos.py                # SOS emergency
│   │   │   └── ai.py                 # AI analysis
│   │   ├── core/
│   │   │   ├── config.py             # Pydantic Settings (env vars)
│   │   │   ├── database.py           # Async SQLAlchemy setup
│   │   │   ├── redis.py              # Redis client
│   │   │   └── security.py           # JWT utilities
│   │   ├── models/                   # SQLAlchemy ORM models
│   │   │   ├── user.py
│   │   │   ├── crime.py
│   │   │   ├── sos.py
│   │   │   └── location.py
│   │   ├── schemas/                  # Pydantic request/response schemas
│   │   ├── services/                 # Business logic layer
│   │   │   ├── ai/
│   │   │   │   └── crime_vision_service.py   # ML Fusion Engine
│   │   │   ├── route_service.py      # OSRM + safety scoring
│   │   │   └── sos_service.py        # SOS orchestration
│   │   └── main.py                   # FastAPI app entry point
│   ├── tests/                        # pytest test suite
│   │   └── test_crime_vision.py      # AI service unit tests
│   ├── scripts/                      # Utility scripts
│   │   └── download_models.py        # YOLOv9c model downloader
│   ├── requirements.txt
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── frontend/                         # React Native mobile app
│   ├── src/
│   │   ├── navigation/               # React Navigation setup
│   │   │   ├── RootNavigator.tsx
│   │   │   ├── AuthNavigator.tsx
│   │   │   └── MainTabNavigator.tsx
│   │   ├── screens/
│   │   │   ├── Auth/                 # Login / Register
│   │   │   ├── Home/                 # Home dashboard
│   │   │   ├── Map/                  # Map & route planning
│   │   │   ├── Reports/              # Crime reporting + AI UI
│   │   │   │   └── AddReportScreen.tsx
│   │   │   ├── Profile/              # User profile & contacts
│   │   │   └── Splash/
│   │   ├── store/                    # Zustand state stores
│   │   │   ├── authStore.ts
│   │   │   └── locationStore.ts
│   │   ├── services/                 # Axios API service layer
│   │   ├── hooks/                    # Custom React hooks
│   │   ├── components/               # Reusable UI components
│   │   └── types/                    # TypeScript type definitions
│   ├── package.json
│   └── app.json
│
├── report/                           # Academic project report
│   ├── nirapodpoint_report.tex       # LaTeX source
│   └── mermaid_diagrams.md           # System design diagram codes
│
└── README.md                         # This file
```

---

## 🚀 Getting Started

### Prerequisites

| Requirement | Version |
|---|---|
| Python | 3.11+ |
| Node.js | 18+ |
| PostgreSQL + PostGIS | 16+ |
| Redis | 7+ |
| Docker (recommended) | Latest |
| Expo CLI | Via npx |

### Quick Start with Docker

```bash
# 1. Clone the repository
git clone https://github.com/ArafatBytes/Nirapod-Point-Mobile-App.git
cd "NirapodPoint App"

# 2. Setup & start the backend
cd backend
cp .env.example .env
# Edit .env with your keys (see Environment Variables section below)
docker-compose up -d

# 3. Setup & start the frontend
cd ../frontend
cp .env.example .env
npm install
npx expo start
```

### Manual Backend Setup

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux / Mac

# Install dependencies
pip install -r requirements.txt

# Download the YOLOv9c model (82 MB)
python scripts/download_models.py

# Configure environment
cp .env.example .env
# Fill in: DATABASE_URL, REDIS_URL, SECRET_KEY, FIREBASE_CONFIG, SUPABASE_URL

# Run database migrations
alembic upgrade head

# Start the development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
# API docs → http://localhost:8000/docs
```

### Manual Frontend Setup

```bash
cd frontend

npm install

cp .env.example .env
# Fill in: EXPO_PUBLIC_API_URL, EXPO_PUBLIC_SUPABASE_URL, EXPO_PUBLIC_SUPABASE_KEY

npx expo start
# Press 'a' → Android emulator
# Press 'i' → iOS simulator (Mac only)
# Scan QR → Expo Go on physical device
```

### Environment Variables

**Backend `.env`:**
```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/nirapodpoint
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-super-secret-jwt-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=your-supabase-key
FIREBASE_CREDENTIALS_PATH=./firebase-adminsdk.json
CLOUDWAVEBD_API_KEY=your-sms-api-key
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

**Frontend `.env`:**
```env
EXPO_PUBLIC_API_URL=http://localhost:8000
EXPO_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
EXPO_PUBLIC_SUPABASE_KEY=your-supabase-anon-key
EXPO_PUBLIC_FIREBASE_API_KEY=your-firebase-api-key
```

### AI Model Setup

AI model weights are **not included** in the repository (too large for Git).

```bash
cd backend
python scripts/download_models.py     # Downloads yolov9c.pt (~82 MB)
```

**Manual download:** https://github.com/WongKinYiu/yolov9/releases → place `yolov9c.pt` in `backend/`

MediaPipe and CLIP models are downloaded automatically on first use and cached locally.

---

## 🤖 AI Pipeline

The **ML Fusion Decision Engine** is the core innovation of NirapodPoint. It runs three models in parallel and combines their outputs using a weighted voting system:

```
       Image Input
           │
    ┌──────┼──────┐
    ▼      ▼      ▼
 YOLOv9c MediaPipe  CLIP
  (40%)   (35%)   (25%)
    │      │       │
    └──────┴───────┘
           │
    ML Fusion Engine
    (weighted voting +
    cross-model agreement)
           │
    Confidence Calibration
           │
    ┌──────┴────────────┐
    │  Crime Type       │
    │  Confidence Score │
    │  Auto-Title       │
    │  Description      │
    └───────────────────┘
```

### Safety Scoring Formula

```
S_safety = 100 − [ 0.3 × R_regional + 0.7 × (100 × (1 − e^(−0.01 × R_local))) ]
```

Logarithmic normalisation prevents dense crime datasets from saturating the score.

---

## 📡 API Reference

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/auth/register` | Register new user |
| `POST` | `/api/v1/auth/login` | Login, receive JWT |
| `GET` | `/api/v1/auth/me` | Get current user |
| `POST` | `/api/v1/crimes/` | Submit crime report |
| `GET` | `/api/v1/crimes/` | List crime reports |
| `POST` | `/api/v1/crimes/{id}/analyze` | Run AI analysis on image |
| `POST` | `/api/v1/routes/calculate` | Calculate safe routes |
| `POST` | `/api/v1/sos/trigger` | Trigger SOS alert |
| `GET` | `/api/v1/profile/` | Get user profile |
| `PUT` | `/api/v1/profile/contacts` | Update emergency contacts |
| `GET` | `/health` | API health check |

Full interactive docs: `http://localhost:8000/docs` (Swagger UI)

---

## 🧪 Testing

### Run Backend Tests

```bash
cd backend
venv\Scripts\activate       # activate virtual environment

# Run all tests
pytest

# Run with coverage report
pytest --cov=app tests/ --cov-report=html

# Run specific test file
pytest tests/test_crime_vision.py -v

# Test AI models individually
python scripts/test_yolov9.py
python scripts/test_mediapipe.py
python scripts/test_clip.py
python scripts/test_ml_fusion.py
```

### Run Frontend Tests

```bash
cd frontend
npm test
npm test -- --coverage
npm test -- AddReportScreen.test.tsx
```

### Test Results Summary

| Category | Tests | Result |
|---|---|---|
| Crime Vision Service | 18 | ✅ All Pass |
| Crime Rule Validation | 3 | ✅ All Pass |
| API Endpoints | 8 | ✅ All Pass |
| **Total** | **29** | **✅ 29/29 Pass** |

---

## 📊 Performance Targets

| Metric | Target | Achieved |
|---|---|---|
| Route calculation | < 2 s | ~1.7 s ✅ |
| Map load time | < 1 s | ~0.8 s ✅ |
| SOS trigger → notification | < 5 s | ~3.2 s ✅ |
| App cold start | < 3 s | ~2.4 s ✅ |
| Battery drain (background) | < 5%/hr | ~3.2%/hr ✅ |
| API uptime SLA | ≥ 99.5% | Monitored |
| AI image analysis | < 10 s | ~5.7 s ✅ |

---

## 📈 Development Roadmap

### ✅ Completed
- [x] YOLOv9c object detection integration
- [x] MediaPipe pose estimation (8 actions, 3 threat levels)
- [x] CLIP scene classification
- [x] ML Fusion Decision Engine (weighted voting + calibration)
- [x] Community crime reporting with AI analysis
- [x] Smart route calculation with safety scoring
- [x] PostgreSQL + PostGIS geospatial backend
- [x] JWT authentication & bcrypt password hashing
- [x] Voice-activated SOS emergency system
- [x] Email + SMS emergency notifications
- [x] Firebase FCM push notifications
- [x] Background GPS tracking & danger zone geofencing

### 🔄 In Progress
- [ ] Offline map tile caching
- [ ] Multi-language voice commands (Bangla, Hindi)

### 🔮 Planned
- [ ] Temporal crime patterns (time-of-day weighting)
- [ ] Community report verification (crowdsourced upvoting)
- [ ] Government / police department API integration
- [ ] Analytics dashboard for law enforcement
- [ ] Real-time WebSocket crime feed

---

## 🔐 Security

- **Authentication**: Stateless JWT with 24-hour expiry
- **Passwords**: bcrypt hashing via `passlib`
- **Transport**: HTTPS enforced for all communication
- **Database**: SQL injection prevented by SQLAlchemy ORM
- **API**: Rate limiting on sensitive endpoints (login, SOS)
- **CORS**: Configured for specific origins only
- **Storage**: Sensitive tokens stored in `expo-secure-store`
- **Privacy**: GDPR-aligned data minimisation — only location and emergency contact data collected

---

## 👥 Team

**Islamic University of Technology**
*Department of Computer Science and Engineering*
*CSE 4510 — Software Engineering and Object-Oriented Design Lab*

| # | Name | Student ID | Role |
|---|---|---|---|
| 1 | **Md. Arafat Ullah** | 220041146 | Backend · AI/ML Pipeline · Project Lead |
| 2 | **G.M Noor Ul Islam Labib** | 220041124 | Backend · Route Service · Database |
| 3 | **Abu Bakar Alam** | 220041108 | Frontend · Map & Navigation |
| 4 | **A.K.M Ferdous Reza Habib** | 220041138 | Frontend · SOS & Notifications |
| 5 | **Rahinur Bin Naushad** | 220041118 | Backend · Auth & Security |
| 6 | **Sheikh Farhan Adib Auvro** | 220041104 | Frontend · UI/UX & State Management |

**Repository**: [github.com/ArafatBytes/Nirapod-Point-Mobile-App](https://github.com/ArafatBytes/Nirapod-Point-Mobile-App)

---

## 🤝 Contributing

We welcome contributions! Follow these steps:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/your-feature`
3. **Commit** your changes: `git commit -m 'Add: your feature description'`
4. **Push** to the branch: `git push origin feature/your-feature`
5. **Open** a Pull Request

### Coding Standards

**Backend (Python):**
- Follow PEP 8 style guide
- Use type hints on all functions
- Write docstrings for classes and public methods
- Run `black .` for formatting
- Run `flake8` for lint checks
- Always activate `venv` before working

**Frontend (TypeScript/React Native):**
- Strict TypeScript — no `any` types
- Functional components + hooks only
- Business logic in custom hooks, not screens
- Run `npm run lint` before committing

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

- [Ultralytics](https://ultralytics.com/) for YOLOv9c
- [HuggingFace](https://huggingface.co/) for CLIP & Transformers
- [Google MediaPipe](https://mediapipe.dev/) for pose estimation
- [OSRM Project](https://project-osrm.org/) for open-source routing
- [OpenStreetMap](https://openstreetmap.org/) for map data
- [Firebase](https://firebase.google.com/) for push notifications
- [CloudWaveBD](https://cloudwavebd.com/) for SMS gateway
- [Supabase](https://supabase.com/) for storage & auth helpers
- The React Native and FastAPI open-source communities

---

<div align="center">

**Built with ❤️ for safer communities**

*NirapodPoint — March 2026*

</div>
