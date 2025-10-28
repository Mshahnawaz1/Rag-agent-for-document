# Docker Setup for AI tutor RAG Application

This guide explains how to run the AI tutor RAG Document Chatbot using Docker and Docker Compose.

## Prerequisites

- Docker Desktop (Windows/Mac) or Docker Engine (Linux)
- Docker Compose v2.0+
- `.env` file with `GOOGLE_API_KEY` set

## Quick Start

1. **Create a `.env` file** in the project root with your Google API key:
   ```env
   GOOGLE_API_KEY=your_api_key_here
   ```

2. **Build and start the containers**:
   ```powershell
   docker-compose up --build
   ```

3. **Access the application**:
   - Frontend: http://localhost
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

4. **Stop the containers**:
   ```powershell
   docker-compose down
   ```

## Services

### Backend (FastAPI)
- **Port**: 8000
- **Container**: `rag-backend`
- **Tech**: Python 3.11, FastAPI, LangChain, ChromaDB
- **Volumes**:
  - `./uploads` → `/app/uploads` (uploaded documents)
  - `./data/chroma_db` → `/app/data/chroma_db` (vector database)

### Frontend (Nginx)
- **Port**: 80
- **Container**: `rag-frontend`
- **Tech**: Nginx Alpine, HTML/JS/TailwindCSS
- **Proxy**: API requests to `/api/*` are proxied to backend

## Docker Commands

### Build and run in detached mode
```powershell
docker-compose up -d --build
```

### View logs
```powershell
# All services
docker-compose logs -f

# Backend only
docker-compose logs -f backend

# Frontend only
docker-compose logs -f frontend
```

### Restart services
```powershell
docker-compose restart
```

### Stop and remove containers, networks
```powershell
docker-compose down
```

### Remove volumes (clears uploads and vector DB)
```powershell
docker-compose down -v
```

## Development Mode

To enable hot-reload for backend code changes, uncomment the volume mount in `docker-compose.yml`:

```yaml
services:
  backend:
    volumes:
      - ./src:/app/src  # Uncomment this line
```

Then restart:
```powershell
docker-compose restart backend
```

## Troubleshooting

### Port already in use
If port 80 or 8000 is already in use, edit `docker-compose.yml`:

```yaml
services:
  backend:
    ports:
      - "8001:8000"  # Change host port
  frontend:
    ports:
      - "8080:80"    # Change host port
```

### Environment variables not loaded
Ensure `.env` file is in the project root and contains valid keys.

### Upload fails
Check that the `uploads/` directory has write permissions:
```powershell
mkdir -p uploads data/chroma_db
```

### Clear vector database
Use the "Clear Index" button in the UI or run:
```powershell
docker-compose exec backend rm -rf /app/data/chroma_db/*
docker-compose restart backend
```

## Production Deployment

For production:
1. Update `nginx.conf` with your domain
2. Add SSL/TLS certificates
3. Set appropriate CORS origins in `src/main.py`
4. Use environment-specific `.env` files
5. Consider using Docker secrets for API keys
6. Add health checks and logging

## Architecture

```
┌─────────────┐
│   Browser   │
└──────┬──────┘
       │ :80
       ▼
┌─────────────┐      ┌──────────────┐
│   Nginx     │─────▶│   FastAPI    │
│  (Frontend) │ :8000│   (Backend)  │
└─────────────┘      └───────┬──────┘
                             │
                    ┌────────┴────────┐
                    │                 │
              ┌─────▼─────┐   ┌──────▼──────┐
              │  Uploads  │   │  ChromaDB   │
              │  Volume   │   │   Volume    │
              └───────────┘   └─────────────┘
```

## Network

All services run on the `rag-network` bridge network, enabling inter-service communication by container name.
