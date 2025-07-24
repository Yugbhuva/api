# FastAPI REST API Template

A production-ready FastAPI REST API template with SQLAlchemy, PostgreSQL, and Docker support.

## Features

- ✅ **FastAPI** with async/await support
- ✅ **SQLAlchemy** ORM with async support
- ✅ **PostgreSQL** (production) and SQLite (development)
- ✅ **Pydantic** schemas for validation
- ✅ **Docker** and docker-compose setup
- ✅ **API versioning** (/api/v1/)
- ✅ **CORS** middleware
- ✅ **Structured logging** with file rotation
- ✅ **Environment-based configuration**
- ✅ **Clean architecture** with separation of concerns
- ✅ **OpenAPI/Swagger** documentation
- ✅ **Basic testing** with pytest

## Quick Start

### 1. Using Docker (Recommended)

```bash
# Clone and setup
git clone <repository>
cd fastapi_rest_template

# Start with docker-compose
docker-compose up --build
```

### 2. Local Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env

# Run the application
uvicorn app.main:app --reload
```

## API Endpoints

- **GET** `/` - Root endpoint
- **GET** `/health` - Health check
- **GET** `/docs` - Swagger UI documentation
- **GET** `/api/v1/items/` - Get all items
- **POST** `/api/v1/items/` - Create new item
- **GET** `/api/v1/items/{id}` - Get item by ID
- **PUT** `/api/v1/items/{id}` - Update item
- **DELETE** `/api/v1/items/{id}` - Delete item

## Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=app
```

## Configuration

The application supports three environments:
- **development**: SQLite database, debug logging
- **production**: PostgreSQL database, file logging with rotation
- **testing**: In-memory SQLite, test-specific settings

Set the `ENVIRONMENT` variable in your `.env` file.

## Project Structure

```
app/
├── api/v1/routes/          # API routes
├── core/                   # Configuration and logging
├── models/                 # SQLAlchemy models
├── schemas/                # Pydantic schemas
├── services/               # Business logic
└── main.py                 # Application entry point
```

## Development

This template follows clean architecture principles:
- **Routes** handle HTTP requests/responses
- **Services** contain business logic
- **Models** define database schema
- **Schemas** handle data validation
- **Core** manages configuration and logging

## License

MIT License
```

## Usage Instructions

1. **Setup Project Structure**: Create the directory structure as shown above
2. **Copy Files**: Place each file in its respective directory
3. **Environment Setup**: Copy `.env.example` to `.env` and modify as needed
4. **Dependencies**: Install requirements with `pip install -r requirements.txt`
5. **Database**: The app will automatically create SQLite tables on startup
6. **Run Application**: Use `uvicorn app.main:app --reload` for development
7. **Docker**: Use `docker-compose up --build` for containerized deployment
8. **Testing**: Run `pytest` to execute the test suite

The template provides a solid foundation for FastAPI applications with proper separation of concerns, environment management, and production-ready features.