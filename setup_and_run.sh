#!/bin/bash

# Exit on error
set -e

echo "🚀 Starting setup for Barkibu Application..."

# 1. Check for Homebrew (macOS Package Manager)
if ! command -v brew &> /dev/null; then
    echo "🍺 Homebrew not found. Installing..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    
    # Add brew to path for immediate use if needed (standard location for Apple Silicon)
    if [ -f "/opt/homebrew/bin/brew" ]; then
        eval "$(/opt/homebrew/bin/brew shellenv)"
    fi
else
    echo "✅ Homebrew is already installed."
fi

# 2. Install Dependencies
echo "📦 Installing dependencies..."

# Docker
if ! command -v docker &> /dev/null; then
    echo "🐳 Installing Docker..."
    brew install --cask docker
else
    echo "✅ Docker is already installed."
fi

# Minikube
if ! command -v minikube &> /dev/null; then
    echo "☸️ Installing Minikube..."
    brew install minikube
else
    echo "✅ Minikube is already installed."
fi

# Kubectl
if ! command -v kubectl &> /dev/null; then
    echo "🎮 Installing Kubectl..."
    brew install kubernetes-cli
else
    echo "✅ Kubectl is already installed."
fi

# Helm
if ! command -v helm &> /dev/null; then
    echo "⛑️ Installing Helm..."
    brew install helm
else
    echo "✅ Helm is already installed."
fi

# 3. Start Docker
echo "🐳 Starting Docker..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    # Try to open Docker Desktop
    open -a Docker
    echo "⏳ Waiting for Docker to start... (this may take a minute)"
    # Wait until docker daemon is responsive
    while ! docker system info > /dev/null 2>&1; do
        sleep 5
        echo "   Still waiting for Docker..."
    done
    echo "✅ Docker is running."
else
    echo "⚠️  Not on macOS. Please ensure Docker daemon is running manually."
fi

# 4. Start Minikube
echo "☸️ Starting Minikube..."
minikube start

# 5. Build Docker Images
echo "🏗️ Building Docker images inside Minikube..."
# Point your terminal's docker-cli to the docker engine inside minikube
eval $(minikube docker-env)

echo "   Building Backend (barkibu:latest)..."
docker build -t barkibu:latest backend

echo "   Building Frontend (barkibu-frontend:latest)..."
docker build -t barkibu-frontend:latest frontend

# 6. Deploy with Helm
echo "🚀 Deploying application..."

# Check if release exists and uninstall if it does to ensure clean slate
if helm list -q | grep -q "^barkibu$"; then
    echo "   Uninstalling existing release..."
    helm uninstall barkibu
fi

# Install the chart
helm install barkibu ./helm/barkibu -f ./helm/barkibu/values/dev.yaml

echo "✅ Deployment complete!"
echo "Waiting for pods to be ready..."
kubectl wait --for=condition=ready pod -l app=barkibu --timeout=120s
kubectl wait --for=condition=ready pod -l app=barkibu-frontend --timeout=120s

minikube service barkibu-frontend
