# Runbook

Common failures and fixes for the MVP Web App.

## Services Won't Start

### Issue: Port already in use

**Symptoms**: Error about port 5432, 8000, or 3000 already in use.

**Common causes**:
- Another Docker container is using the port (e.g., `dataops-postgres` using 5432)
- A local service is running on the port (e.g., local PostgreSQL installation)

**Fix**:
1. Check what's using the port:
   ```bash
   # Check Docker containers
   docker ps | grep <port>
   
   # Check system processes
   lsof -i :<port>  # or `netstat -tulpn | grep :<port>`
   ```

2. **Option A: Change port in `.env`** (Recommended if you have other services):
   ```bash
   # Edit .env file
   POSTGRES_PORT=5433  # Use a different port
   BACKEND_PORT=8001   # If 8000 is also in use
   FRONTEND_PORT=3001   # If 3000 is also in use
   ```

3. **Option B: Stop conflicting Docker container** (if safe to do so):
   ```bash
   docker stop <container-name>
   ```

**Example**: If `dataops-postgres` is using port 5432:
- Change `POSTGRES_PORT=5433` in `.env` (recommended)
- Or stop it: `docker stop dataops-postgres` (only if you don't need it)

### Issue: Docker Compose version

**Symptoms**: `docker compose` command not found.

**Fix**:
- Use `docker-compose` (with hyphen) if Docker Compose v1 is installed
- Or upgrade to Docker Compose v2: `sudo apt-get update && sudo apt-get install docker-compose-plugin`

## Database Issues

### Issue: Database connection refused

**Symptoms**: Backend logs show "connection refused" or "could not connect to server".

**Fix**:
1. Check PostgreSQL is running: `docker compose ps`
2. Check PostgreSQL logs: `docker compose logs postgres`
3. Ensure backend depends_on postgres with healthcheck
4. Wait for postgres healthcheck to pass before backend starts

### Issue: Migration errors

**Symptoms**: Alembic migration fails or tables don't exist.

**Fix**:
1. Reset database: `docker compose down -v && docker compose up`
2. Manually run migrations: `docker compose exec backend alembic upgrade head`
3. Check migration files in `backend/alembic/versions/`

### Issue: Seed data not appearing

**Symptoms**: No items visible after startup.

**Fix**:
1. Check seed script ran: `docker compose logs backend | grep seed`
2. Manually run seed: `docker compose exec backend python scripts/seed.py`
3. Verify database: `docker compose exec postgres psql -U appuser -d appdb -c "SELECT * FROM items;"`

## Backend Issues

### Issue: Import errors

**Symptoms**: `ModuleNotFoundError` or import errors.

**Fix**:
1. Ensure dependencies installed: `docker compose exec backend pip install -r requirements.txt`
2. Check Python path and virtual environment
3. Rebuild container: `docker compose build backend`

### Issue: API returns 500 errors

**Symptoms**: Frontend shows errors, backend logs show exceptions.

**Fix**:
1. Check backend logs: `docker compose logs backend`
2. Verify database connection and schema
3. Check environment variables: `docker compose exec backend env | grep POSTGRES`

## Frontend Issues

### Issue: Cannot connect to API

**Symptoms**: Network errors, CORS errors, or "Failed to fetch".

**Fix**:
1. Check `NEXT_PUBLIC_API_URL` in `.env` matches backend URL
2. In Docker, use service name: `http://backend:8000` (internal) or `http://localhost:8000` (browser)
3. Check CORS settings in backend
4. Verify backend is running: `curl http://localhost:8000/healthz`

### Issue: Build errors

**Symptoms**: Frontend container fails to start or build.

**Fix**:
1. Check Node version compatibility
2. Clear cache: `docker compose down && docker compose build --no-cache frontend`
3. Check `node_modules` permissions in WSL2

## WSL2 Specific Issues

### Issue: File permissions

**Symptoms**: Permission denied errors when accessing files.

**Fix**:
1. Check file ownership: `ls -la`
2. Fix ownership: `sudo chown -R $USER:$USER .`
3. Ensure Docker Desktop has access to WSL2 filesystem

### Issue: Slow file watching

**Symptoms**: Hot reload is slow or doesn't work.

**Fix**:
1. Use Docker volumes (already configured)
2. Consider using `polling` option in Next.js config for WSL2
3. Check Docker Desktop resource allocation

## Clean Slate Reset

If everything is broken, start fresh:

```bash
# Stop and remove everything
docker compose down -v

# Remove images (optional)
docker compose down --rmi all

# Clean build
docker compose build --no-cache

# Start fresh
docker compose up
```

## Logs

View logs for debugging:

```bash
# All services
docker compose logs

# Specific service
docker compose logs backend
docker compose logs frontend
docker compose logs postgres

# Follow logs
docker compose logs -f backend
```

## Health Checks

Verify services are healthy:

```bash
# Backend health
curl http://localhost:8000/healthz

# Database connection
docker compose exec postgres pg_isready -U appuser

# Frontend (check browser console)
curl http://localhost:3000
```

