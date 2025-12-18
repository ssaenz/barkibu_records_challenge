# Barkibu Monorepo

This repository contains the source code for the Barkibu application, including the backend API, frontend application, and infrastructure configuration.

## High level Code organization

- `backend/`: FastAPI application (Python)
- `frontend/`: React application (TypeScript)
- `helm/`: Kubernetes Helm charts for deployment

## Local Deployment (Minikube)

### System Requirements

To run this application locally, you will need the following tools installed on your system. A setup script is provided to install them automatically on macOS.

- **Docker**: Container runtime.
- **Minikube**: Local Kubernetes cluster.
- **Kubectl**: Kubernetes command-line tool.
- **Helm**: Package manager for Kubernetes.

### Automated Setup (macOS)

You can use the provided script to install dependencies and deploy the application in one go:

```bash
./setup_and_run.sh
```

### Manual Deployment

1. Start Minikube:
   ```bash
   minikube start
   eval $(minikube -p minikube docker-env)
   ```

2. Build Backend Image:
   ```bash
   docker build -t barkibu-backend:latest backend
   ```

3. Build Frontend Image:
   ```bash
   docker build -t barkibu-frontend:latest frontend
   ```

4. Deploy with Helm:
   ```bash
   helm upgrade --install barkibu ./helm/barkibu -f ./helm/barkibu/values/dev.yaml
   ```

5. Access the Application:
   ```bash
   minikube service barkibu-frontend
   ```

