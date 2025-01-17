# Docker Website

A web application featuring a chatbot specialized in Docker knowledge.

## Project Structure

```
docker_website/
├── .credentials/          # Store API keys and sensitive data
│   └── openai.env        # OpenAI API key
├── backend/
│   ├── main.py           # FastAPI server
│   ├── chatgpt.py        # ChatGPT service
│   ├── requirements.txt  # Python dependencies
│   └── Dockerfile        # Backend container configuration
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── main.jsx     # Entry point
│   │   └── index.css    # Styles
│   ├── index.html
│   └── package.json     # Node dependencies
└── docker-compose.yml    # Docker services configuration
```

## Setup

### Prerequisites
- Docker
- Node.js (for local frontend development)
- Python 3.11+ (for local backend development)

### Environment Variables
Create `.credentials/openai.env` with your OpenAI API key:
```
OPENAI_API_KEY=your_key_here
```

### Running with Docker
```bash
docker compose up --build
```

### Running Locally

Backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Frontend:
```bash
cd frontend
npm install
npm run dev
```

## API Endpoints

- `GET /health` - Health check endpoint
- `POST /chat` - Chat endpoint
```bash
curl -X POST http://localhost:8000/chat \
-H "Content-Type: application/json" \
-d '{"message": "What is Docker?"}'
```

## Development

The frontend runs on http://localhost:5173
The backend runs on http://localhost:8000

# Deployment to Cloud Run
1. Configure GCP project:
```bash
gcloud init --configuration=chatbot-deploy
gcloud config set project fluted-citizen-269819
gcloud config set run/region us-central1
```
2. Deploy the service:
```bash
./deploy.sh
```
3. Test the deployment:
```bash
./tests/test_deploy.sh
```