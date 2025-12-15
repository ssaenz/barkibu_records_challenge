# Barkibu Medical Records Processing System

An intelligent system for extracting and structuring veterinary medical records from various document formats (PDF, images, Word, etc.).

## Overview

Barkibu helps veterinarians quickly access and interpret medical information by:

- Uploading documents in any format (PDF, JPG, PNG, DOCX, TXT)
- Automatically extracting text content
- Structuring medical data (diagnoses, treatments, pet info, dates)
- Reviewing and editing extracted information
- Accessing standardized medical records

## Prerequisites & Local Development Setup

### System Requirements

Before starting, ensure you have the following tools installed:

#### 1. Python 3.12+

Check if installed:

```bash
python --version
```

If not installed, install via [python.org](https://www.python.org) or Homebrew:

```bash
brew install python@3.12
```

#### 2. Docker

Required for containerization and Kubernetes testing.

Install via [Docker Desktop](https://www.docker.com/products/docker-desktop) or Homebrew:

```bash
brew install docker
brew install colima  # Required for Docker CLI on macOS without Docker Desktop
colima start
```

#### 3. Minikube

Required for local Kubernetes cluster testing.

Install via Homebrew:

```bash
brew install minikube
```

Start Minikube:

```bash
minikube start
```

#### 4. kubectl

Kubernetes command-line tool.

Install via Homebrew:

```bash
brew install kubectl
```

Or via Minikube:

```bash
minikube kubectl -- version
```

#### 5. Helm

Kubernetes package manager.

Install via Homebrew:

```bash
brew install helm
```

### Python Virtual Environment Setup

1. Create and activate virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -e .
```

## Setup

### Running Locally

1. Create and activate virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

Or with pyproject.toml:

```bash
pip install -e .
```

## Run the API

```bash
uvicorn app.main:app --reload
```

## Run tests

```bash
pytest
```

## Docker

To run the application in a Docker container:

1. Build the image:

```bash
docker build -t barkibu .
```

2. Run the container:

```bash
docker run -p 8000:8000 barkibu
```

The API will be available at http://localhost:8000

## Kubernetes

To deploy the application to a Kubernetes cluster:

1. Build and push the Docker image to your registry:

```bash
docker build -t your-registry/barkibu:latest .
docker push your-registry/barkibu:latest
```

2. Update the image reference in `k8s-deployment.yaml` if needed.

3. Apply the Kubernetes manifests:

```bash
kubectl apply -f k8s-deployment.yaml
```

4. Check the deployment status:

```bash
kubectl get pods
kubectl get services
```

The service will be accessible within the cluster at `barkibu-service:8000`

## Helm Deployment

To deploy the application using Helm:

### Local Development (Minikube)

```bash
# Build image in Minikube
eval $(minikube docker-env)
docker build -t barkibu:latest .

# Deploy with dev values
helm install barkibu ./helm/barkibu -f ./helm/barkibu/values/dev.yaml

# Or upgrade existing release
helm upgrade barkibu ./helm/barkibu -f ./helm/barkibu/values/dev.yaml
```

### Check Deployment

```bash
# List Helm releases
helm list

# Get release details
helm status barkibu

# Check pods
kubectl get pods -l app=barkibu

# Get service URL
minikube service barkibu-service --url
```

### Adding New Environments

To add a new environment (e.g., staging, production):

1. Create a new values file:

```bash
cp ./helm/barkibu/values/dev.yaml ./helm/barkibu/values/<env-name>.yaml
```

2. Update the values for your environment

3. Deploy:

```bash
helm install barkibu ./helm/barkibu -f ./helm/barkibu/values/<env-name>.yaml
```
