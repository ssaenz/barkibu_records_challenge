# Barkibu Medical Records API

## Prerequisites & Local Development Setup

### System Requirements

Before starting, ensure you have the following tools installed:

#### 1. Python 3.12+

NOTE: This is only required for local execution. To run with docker this depencency can be skiped.

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

### Running Locally (Python)

1. Create and activate virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -e .
```

3. Run the API:

```bash
uvicorn app.main:app --reload
```

4. Run tests:

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

## Kubernetes (Helm)

To deploy the application to a Kubernetes cluster using Helm:

### Local Development (Minikube)

1. Start Minikube:

```bash
minikube start
```

2. Point Docker to Minikube's daemon:

```bash
eval $(minikube -p minikube docker-env)
```

3. Build the image directly in Minikube (run from `backend/` directory):

```bash
docker build -t barkibu:latest .
```

4. Deploy with Helm using development values (run from project root):

```bash
# Install or Upgrade
helm upgrade --install barkibu ./helm/barkibu -f ./helm/barkibu/values/dev.yaml
```

5. Verify Deployment:

```bash
# Check pods (you should see app and postgres pods)
kubectl get pods

# Check logs if needed
kubectl logs -l app=barkibu
```

6. Access the Application:

```bash
# Get the service URL
minikube service barkibu-service --url

# Test health endpoint
curl $(minikube service barkibu-service --url)/health
```

### Production / Other Environments

To deploy to other environments (staging, prod):

1. Create a new values file (e.g., `values/prod.yaml`) with specific configuration.
2. Deploy using that file:

```bash
helm upgrade --install barkibu ./helm/barkibu -f ./helm/barkibu/values/prod.yaml
```
