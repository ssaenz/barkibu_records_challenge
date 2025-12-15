# Barkibu

A FastAPI REST API project.

## Setup

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
