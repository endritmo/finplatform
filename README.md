# FinPlatform — Microservices Edition

Migrated from a Django monolith to a three-service architecture:

```
finplatform/
├── frontend/          Nginx + plain HTML/CSS/JS (no server-side rendering)
├── backend/           Django REST API + Gunicorn (pure JSON, no templates)
├── database/          SQLite file (bind-mounted in Docker; PVC in Kubernetes)
├── k8s/               Kubernetes manifests
└── docker-compose.yml Local development stack
```

## Local Development (Docker Compose)

```bash
cd finplatform

# 1. Create your .env file
cp .env.example .env
# Fill in SECRET_KEY, GROQ_API_KEY, NEWS_API_KEY

# 2. Start the full stack
docker compose up --build

# App:  http://localhost
# API:  http://localhost:8000/api/
# Admin: http://localhost:8000/admin/
```

## Local Development (without Docker)

```bash
# Terminal 1 — Backend
cd finplatform/backend
pip install -r requirements.txt
cp .env.example .env    # fill in values
python manage.py migrate
python manage.py runserver 8000

# Terminal 2 — Frontend
cd finplatform/frontend
python -m http.server 3000
# Open http://localhost:3000
```

When running without Docker, update the fetch URLs in `frontend/js/api.js`:
```js
const API_BASE = 'http://localhost:8000';
```

## API Reference

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET    | /api/health/                       | No   | Health check |
| POST   | /api/signup/                       | No   | Register |
| POST   | /api/login/                        | No   | Login → JWT |
| POST   | /api/logout/                       | Yes  | Logout |
| GET    | /api/me/                           | Yes  | Current user |
| GET    | /api/symbols/                      | No   | Symbol list |
| GET    | /api/calendar/                     | No   | Events |
| GET    | /api/forum/threads/                | No   | Thread list |
| POST   | /api/forum/threads/create/         | Yes  | New thread |
| GET    | /api/forum/threads/<pk>/           | No   | Thread detail |
| PUT    | /api/forum/threads/<pk>/edit/      | Yes  | Edit thread |
| POST   | /api/forum/threads/<pk>/replies/   | Yes  | Post reply |
| PUT    | /api/forum/replies/<pk>/edit/      | Yes  | Edit reply |
| DELETE | /api/forum/replies/<pk>/delete/    | Yes  | Delete reply |
| POST   | /ai/ask/                           | No   | AI chat |

## Kubernetes

See `k8s/README.md` for the full deployment guide.
