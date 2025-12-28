# MVP Web App

A minimal but complete MVP demonstrating an end-to-end flow: UI → API → DB → UI.

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
- PostgreSQL on port 5432
- Backend API on port 8000
- Frontend on port 3000

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
black .
flake8 .
```

Frontend:
```bash
cd frontend
pnpm lint
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

## Demo Steps

1. Start services: `docker compose up`
2. Wait for all services to be healthy
3. Open http://localhost:3000
4. You should see a list of items (seed data)
5. Create a new item using the form
6. Delete an item using the delete button
7. Verify changes persist after refresh

## API Endpoints

- `GET /healthz` - Health check
- `GET /api/items` - List all items
- `POST /api/items` - Create a new item
- `GET /api/items/{id}` - Get a specific item
- `DELETE /api/items/{id}` - Delete an item

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

