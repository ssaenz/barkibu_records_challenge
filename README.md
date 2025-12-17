# Barkibu Monorepo

This repository contains the source code for the Barkibu application, including the backend API, frontend application, and infrastructure configuration.

## Project Structure

- `backend/`: FastAPI application (Python)
- `frontend/`: React application (TypeScript)
- `helm/`: Kubernetes Helm charts for deployment

## Getting Started

Please refer to the README files in each directory for specific instructions:

- [Backend Documentation](backend/README.md)
- [Frontend Documentation](frontend/README.md)

## Full Stack Deployment (Minikube)

1. Start Minikube:
   ```bash
   minikube start
   eval $(minikube -p minikube docker-env)
   ```

2. Build Backend Image:
   ```bash
   cd backend
   docker build -t barkibu:latest .
   cd ..
   ```

3. Build Frontend Image:
   ```bash
   cd frontend
   docker build -t barkibu-frontend:latest .
   cd ..
   ```

4. Deploy with Helm:
   ```bash
   helm upgrade --install barkibu ./helm/barkibu -f ./helm/barkibu/values/dev.yaml
   ```

5. Access the Application:
   - Backend API: `minikube service barkibu-service --url`
   - Frontend: `minikube service barkibu-frontend --url`

