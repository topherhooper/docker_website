
# Docker Website

A web application featuring a Docker-specialized chatbot assistant built with React and FastAPI.

## Technology Stack

- **Frontend:** React + Vite + TailwindCSS
- **Backend:** Python FastAPI
- **Container:** Docker
- **Authentication:** Google OAuth2
- **CI/CD:** GitHub Actions + Google Cloud Run

## Prerequisites

- Docker and Docker Compose
- Google Cloud Platform account (for deployment)
- Node.js 18+ (for local frontend development)
- Python 3.11+ (for local backend development)

## Quick Start

1. Setup credentials:
```sh
# Create credentials directory
mkdir .credentials

# Setup OpenAI API key
echo "OPENAI_API_KEY=your_key_here" > .credentials/openai.env

# Setup Google OAuth credentials (required for auth)
# Copy your Google OAuth credentials JSON to:
.credentials/frontend_google_oath.json
```

2. Start the application:
```sh
docker compose up --build
```

3. Access the application:
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000

## Development

The application uses Docker with hot-reload for development:
- Frontend container (React): Port 5173
- Backend container (FastAPI): Port 8000

### Project Structure

```
.
├── frontend/               # React frontend
│   ├── src/               # Source code
│   ├── tests/             # Frontend tests
│   └── Dockerfile         # Frontend container config
├── backend/               # Python FastAPI backend
│   ├── tests/             # Backend tests
│   └── Dockerfile         # Backend container config
├── .github/workflows/     # GitHub Actions CI/CD
└── docker-compose.yml     # Local development config
```

## Testing

Run all tests:
```sh
make test
```

Run specific tests:
```sh
# Backend tests
make test-backend

# Frontend tests
make test-frontend
```

## Deployment

The application deploys automatically to Google Cloud Run on pushes to the master branch.

Manual deployment:
```sh
# Deploy both services
make deploy-all

# Deploy specific service
make deploy-backend
make deploy-frontend
```

## API Endpoints

- `GET /health` - Health check endpoint
- `POST /chat` - Chat endpoint (requires authentication)
- `POST /verify_token` - Google OAuth token verification

## License

This project is licensed under the MIT License.