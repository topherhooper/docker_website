.PHONY: build deploy-backend deploy-frontend deploy-all clean dev check

# Build commands
build-backend:
	@echo "Building backend..."
	cd backend && docker build -t docker-assistant-backend .

build-frontend:
	@echo "Building frontend..."
	cd frontend && docker build -t docker-assistant-frontend .

build: build-backend build-frontend

# Deploy commands
deploy-backend:
	@echo "Deploying backend service..."
	cd backend && ./deploy.sh

deploy-frontend:
	@echo "Deploying frontend service..."
	cd frontend && ./deploy.sh

deploy-all: deploy-backend deploy-frontend
	@echo "Deployment complete!"

# Development commands
dev-backend:
	@echo "Starting backend in dev mode..."
	cd backend && docker-compose up

dev-frontend:
	@echo "Starting frontend in dev mode..."
	cd frontend && npm run dev

# Clean commands
clean-backend:
	@echo "Cleaning backend..."
	docker rmi docker-assistant-backend || true
	cd backend && rm -rf node_modules

clean-frontend:
	@echo "Cleaning frontend..."
	docker rmi docker-assistant-frontend || true
	cd frontend && rm -rf node_modules

clean: clean-backend clean-frontend

# Check deployment status
check:
	@echo "Checking backend status..."
	cd backend/tests && ./test_deploy.sh
	@echo "Checking frontend URL..."
	gcloud run services describe chatbot-frontend --platform managed --region us-central1 --format 'value(status.url)'

# Help
help:
	@echo "Available targets:"
	@echo "  build          - Build both services"
	@echo "  deploy-backend - Deploy the backend service"
	@echo "  deploy-frontend- Deploy the frontend service"
	@echo "  deploy-all     - Deploy both services"
	@echo "  dev-backend    - Start backend in dev mode"
	@echo "  dev-frontend   - Start frontend in dev mode"
	@echo "  clean          - Clean both services"
	@echo "  check          - Check deployment status"