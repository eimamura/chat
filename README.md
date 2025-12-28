# Chat MVP

A minimal but complete chat application demonstrating an end-to-end flow: UI → API → DB → UI.

## Tech Stack

- **Frontend**: Next.js (App Router) + TypeScript
- **Backend**: FastAPI (Python) + Uvicorn
- **Database**: PostgreSQL
- **Migrations**: Alembic
- **Container**: Docker Compose v2

## Prerequisites

- Docker and Docker Compose v2
- WSL2 Ubuntu (for Windows users)
- Git

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd chat
```

2. Copy environment variables:
```bash
cp .env.example .env
```

3. Review and adjust `.env` if needed (defaults should work for local dev).

## Run

Start all services with Docker Compose:

```bash
docker compose up
```

This will start:
- PostgreSQL on port 5433 (configurable via `POSTGRES_PORT` in `.env`)
- Backend API on port 8000
- Frontend on port 3000

**Note**: If port 5432 is already in use (e.g., by another PostgreSQL instance), the default port is set to 5433. You can change this in `.env` if needed.

Access:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs (OpenAPI): http://localhost:8000/docs
- Health Check: http://localhost:8000/healthz

## Test

### Backend Tests

```bash
cd backend
python -m pytest
```

Or with Docker:
```bash
docker compose exec backend pytest
```

### Frontend Tests

```bash
cd frontend
pnpm test
```

### Lint/Format

Backend:
```bash
cd backend
# Format code
black .

# Lint code
flake8 .

# Run tests
pytest
```

Frontend:
```bash
cd frontend
# Lint code
pnpm lint

# Format code
pnpm format
```

## Reset DB / Clean Volumes

To reset the database and start fresh:

```bash
docker compose down -v
docker compose up
```

This will:
- Remove all containers
- Remove the PostgreSQL volume (all data will be lost)
- Start fresh with migrations and seed data

### Manual Database Reset

If you need to reset just the database without removing volumes:

```bash
# Connect to database
docker compose exec postgres psql -U appuser -d appdb

# In psql, drop and recreate:
# DROP TABLE messages;
# \q

# Then run migrations
docker compose exec backend alembic upgrade head

# Seed data
docker compose exec backend python scripts/seed.py
```

## Demo Steps

### Quick Demo (Automated)

Run the demo script to verify end-to-end functionality:

```bash
./scripts/demo.sh
```

### Manual Demo

1. Start services: `docker compose up`
2. Wait for all services to be healthy (check logs: `docker compose logs`)
3. Open http://localhost:3000 in your browser
4. You should see sample chat messages (seed data - 5 messages)
5. Enter your username in the input field at the top
6. Type a message and click "Send"
7. Your message should appear in the chat
8. Messages auto-refresh every 3 seconds to show new messages from other users

## API Endpoints

- `GET /healthz` - Health check
- `GET /api/messages` - List all messages (ordered chronologically)
  - Query params: `limit` (optional, 1-100) - Limit number of messages
- `POST /api/messages` - Create a new message
  - Body: `{ "username": "string", "content": "string" }`
- `GET /api/messages/{id}` - Get a specific message
- `DELETE /api/messages/{id}` - Delete a message

Full API documentation available at `/docs` (OpenAPI/Swagger UI).

## Project Structure

```
.
├── backend/          # FastAPI application
│   ├── app/
│   ├── alembic/      # Database migrations
│   └── tests/
├── frontend/         # Next.js application
│   ├── app/
│   └── components/
├── compose.yaml      # Docker Compose configuration
└── README.md

```

## Development

### Backend Development

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend Development

```bash
cd frontend
pnpm install
pnpm dev
```

## Troubleshooting

See `RUNBOOK.md` for common issues and solutions.

