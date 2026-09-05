# Network Backend

## Project Setup

### 1. Create and activate a virtual environment

On Windows:

```powershell
python -m venv venv
venv\Scripts\activate
```

### 2. Install dependencies

```powershell
poetry install
```

### 3. Enable Redis cache[optional]

Switch to the Redis cache branch:

```powershell
git checkout feature/redis-cache
```

Start Redis with Docker:

```powershell
docker run --name django-redis -d -p 6380:6379 redis
```

### 4. Apply database migrations

```powershell
poetry run python manage.py migrate
```

### 5. Start the application

```powershell
poetry run python manage.py runserver
```

The application runs at `http://127.0.0.1:8000/`.

### 6. Open Swagger UI

Swagger UI is available at:

`http://127.0.0.1:8000/api/docs/`
