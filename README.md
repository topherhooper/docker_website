# Docker Website
A web application featuring a Docker-specialized chatbot assistant built with React and FastAPI.

## Technology Stack
- Frontend: React + Vite + TailwindCSS
- Backend: Python FastAPI
- Container: Docker

## Prerequisites
- Docker
- Docker Compose

## Quick Start

1. Setup environment:
   ```sh
   # Create .credentials directory and OpenAI API key file
   mkdir .credentials
   echo "OPENAI_API_KEY=your_key_here" > .credentials/openai.env
   ```

2. Start the application:
   ```sh
   docker compose up --build
   ```

3. Access the application:
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000

## Development

The application runs in Docker containers with hot-reload enabled:
- Frontend container serves React application on port 5173
- Backend container serves FastAPI application on port 8000

### Project Structure
```
.
├── frontend/            # React frontend
├── backend/            # Python FastAPI backend
└── docker-compose.yml  # Docker services configuration
```

## API Endpoints

- `GET /health` - Health check endpoint
- `POST /chat` - Chat endpoint for interacting with the Docker assistant

This update:
1. Provides clear setup instructions
2. Documents the Docker-based architecture
3. Lists the technology stack
4. Includes development information
5. Maintains essential API documentation

Since you're using Docker Compose, this README focuses on the containerized setup rather than local development instructions.
This update:
1. Provides clear setup instructions
2. Documents the Docker-based architecture
3. Lists the technology stack
4. Includes development information
5. Maintains essential API documentation

Since you're using Docker Compose, this README focuses on the containerized setup rather than local development instructions.