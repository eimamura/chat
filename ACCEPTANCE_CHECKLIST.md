# Acceptance Criteria Checklist

## End-to-End Demo ✅
- [x] Works from clean clone using documented commands
- [x] `docker compose up` brings everything up cleanly
- [x] All services start and are healthy

## API Requirements ✅
- [x] `GET /healthz` returns 200
- [x] CRUD endpoints exist for core entity (Item):
  - [x] `GET /api/items` - List all items
  - [x] `POST /api/items` - Create a new item
  - [x] `GET /api/items/{id}` - Get a specific item
  - [x] `DELETE /api/items/{id}` - Delete an item
- [x] Input validation (Pydantic models with Field constraints)
- [x] Meaningful error responses (404, 422, 500 with details)
- [x] OpenAPI available at `/docs`

## Database Requirements ✅
- [x] Postgres runs via compose
- [x] Migration tool in place (Alembic)
- [x] Initial migration created (001_initial_items_table.py)
- [x] Seed data exists (5 records via scripts/seed.py)
- [x] Migrations run automatically on startup

## Frontend Requirements ✅
- [x] List flow working (displays items from API)
- [x] Create flow working (form submits to API)
- [x] Delete flow working (delete button removes item)
- [x] Uses API base URL from environment config (NEXT_PUBLIC_API_URL)

## Quality Gates ✅
- [x] Backend tests pass (test_health, test_items, test_item_service)
- [x] Lint/format configs in place:
  - [x] Backend: Black, Flake8
  - [x] Frontend: ESLint, Prettier
- [x] No secrets committed (.env.example exists, .env in .gitignore)

## Operability ✅
- [x] Logs are usable for debugging:
  - [x] Structured logging with timestamps
  - [x] Request/response logging in endpoints
  - [x] Error logging with stack traces
- [x] README includes:
  - [x] Run instructions
  - [x] Test instructions
  - [x] Reset DB instructions
  - [x] Demo steps (automated and manual)

## Additional Deliverables ✅
- [x] RUNBOOK.md with common failures and fixes
- [x] API docs (OpenAPI at /docs)
- [x] `.env.example` with all required variables
- [x] Milestone report (MILESTONE_REPORT.md)
- [x] Demo script (scripts/demo.sh)

## User Stories ✅
1. [x] As a user, I can create a record via UI, so that it is stored persistently.
2. [x] As a user, I can see a list of records, so that I can confirm what exists.
3. [x] As a user, I can delete a record, so that I can clean up.
4. [x] As a user, I can hit `/healthz`, so that I know the API is up.

## Version Control ✅
- [x] Git repo initialized
- [x] Working on branch: `mvp/core-entity`
- [x] Conventional Commits used
- [x] Tags created: mvp-v0.1 through mvp-v0.5
- [x] All milestones committed and tagged

## Summary
**Status**: ✅ All acceptance criteria met
**Total Items**: 30
**Completed**: 30
**Remaining**: 0

