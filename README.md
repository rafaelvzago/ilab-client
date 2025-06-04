# iLab Client

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/flask-2.3.3-green.svg)](https://flask.palletsprojects.com/)

A Flask web application that serves as a client interface for interacting with AI language model APIs. Provides both a user-friendly web interface and RESTful API endpoints for programmatic access.

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Prerequisites](#-prerequisites)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [API Reference](#-api-reference)
- [Deployment](#-deployment)
  - [Docker/Podman](#dockerpodman)
  - [Kubernetes](#kubernetes)
  - [Istio Service Mesh](#istio-service-mesh)
- [Development](#-development)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

- **Interactive Web Interface**: Clean, responsive UI built with Tailwind CSS
- **RESTful API**: Programmatic access via `/api/completions` endpoint
- **Container Ready**: Docker and Podman support with multi-stage builds
- **Kubernetes Native**: Complete manifests for cluster deployment
- **Istio Compatible**: Service mesh integration with traffic management
- **Health Checks**: Built-in liveness and readiness probes
- **Resource Management**: Configurable CPU and memory limits

## 🏗️ Architecture

This application consists of two main components:

### Frontend
- **Technology**: HTML5 with Tailwind CSS
- **Features**: Single-page application with real-time question/answer interface
- **Location**: `templates/index.html`

### Backend
- **Technology**: Flask (Python)
- **Function**: API proxy that forwards requests to external AI services
- **Endpoint**: Exposes `/api/completions` that proxies to AI service's `/v1/completions`
- **Protocol**: OpenAI-compatible API format

### Data Flow
```
User → Web Interface → Flask App → AI Service (OpenAI-compatible)
                    ↓
              API Response ← AI Service Response
```

## 📋 Prerequisites

- **Python**: 3.10 or higher
- **Package Manager**: pip
- **Container Runtime**: Docker or Podman (optional)
- **Build Tools**: Make (optional)
- **Kubernetes**: kubectl (for cluster deployment)
- **Service Mesh**: Istio (optional, for service mesh deployment)

## 🚀 Quick Start

```bash
# Clone and setup
git clone https://github.com/rafaelvzago/ilab-client.git
cd ilab-client

# Install and run
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Access the application at http://localhost:5000

## 🔧 Installation

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/rafaelvzago/ilab-client.git
   cd ilab-client
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Verify Installation

```bash
python app.py
# Should start server on http://0.0.0.0:5000
```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `ADDRESS` | AI service API URL | `http://127.0.0.1:8000` | Yes |
| `FLASK_ENV` | Flask environment | `production` | No |
| `FLASK_DEBUG` | Enable debug mode | `False` | No |

### Configuration Examples

**Local development:**
```bash
export ADDRESS="http://localhost:8000"
export FLASK_ENV="development"
export FLASK_DEBUG="True"
```

**Production deployment:**
```bash
export ADDRESS="https://api.your-aiservice.com"
```

**Docker environment:**
```bash
docker run -e ADDRESS="https://api.your-aiservice.com" ilab-client
```

## 🎯 Usage

### Web Interface

1. **Start the application**
   ```bash
   python app.py
   ```

2. **Open browser**
   Navigate to http://localhost:5000

3. **Submit questions**
   Use the text area to enter questions and receive AI-generated responses

### Command Line Testing

```bash
# Test API endpoint
curl -X POST http://localhost:5000/api/completions \
  -H "Content-Type: application/json" \
  -d '{"question": "What is artificial intelligence?"}'
```

## 📚 API Reference

### POST `/api/completions`

Submit a question to the AI service and receive a completion.

**Request:**
```http
POST /api/completions
Content-Type: application/json

{
  "question": "Your question here"
}
```

**Response:**
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "response": "AI-generated response text"
}
```

**Error Response:**
```http
HTTP/1.1 400 Bad Request
Content-Type: application/json

{
  "error": "Question is required"
}
```

### GET `/`

Serves the main web interface.

**Response:**
```http
HTTP/1.1 200 OK
Content-Type: text/html

<!-- HTML content -->
```

## 🚀 Deployment

### Docker/Podman

#### Using Makefile (Recommended)

**Build locally:**
```bash
make build
```

**Build and tag for registry:**
```bash
make build-registry REGISTRY=quay.io/your-username IMAGE_TAG=v1.0.0
```

**Build and push to registry:**
```bash
make push REGISTRY=quay.io/your-username IMAGE_TAG=v1.0.0
```

**Clean up images:**
```bash
make clean
```

**Run container:**
```bash
# Local image
podman run -d -p 5000:5000 --name ilab-client ilab-client:latest

# Registry image
podman run -d -p 5000:5000 --name ilab-client quay.io/your-username/ilab-client:v1.0.0
```

#### Manual Docker Commands

**Build and run:**
```bash
# Build image
docker build -t ilab-client .

# Run with default settings
docker run -d -p 5000:5000 --name ilab-client ilab-client

# Run with custom AI service
docker run -d -p 5000:5000 \
  -e ADDRESS="https://api.your-aiservice.com" \
  --name ilab-client ilab-client
```

### Kubernetes

The `manifests/` directory contains Kubernetes resources:

- `deployment.yaml` - Application deployment with health checks
- `service.yaml` - ClusterIP service for internal access
- `gateway.yaml` - Istio Gateway for ingress (Istio only)
- `virtualservice.yaml` - Istio VirtualService for routing (Istio only)

#### Standard Kubernetes Deployment

```bash
# Create namespace
kubectl create namespace ilab-chat

# Deploy application
kubectl apply -f manifests/deployment.yaml -n ilab-chat
kubectl apply -f manifests/service.yaml -n ilab-chat

# Check deployment
kubectl get pods -n ilab-chat
kubectl get services -n ilab-chat
```

#### OpenShift Deployment

```bash
# Create project
oc new-project ilab-chat

# Deploy application
oc apply -f manifests/ -n ilab-chat

# Check deployment
oc get pods -n ilab-chat
oc get routes -n ilab-chat
```

### Istio Service Mesh

#### Prerequisites

- Istio installed in cluster
- Istio ingress gateway configured

#### Deployment Steps

1. **Enable Istio injection**
   ```bash
   kubectl label namespace ilab-chat istio-injection=enabled
   ```

2. **Deploy application**
   ```bash
   kubectl apply -f manifests/ -n ilab-chat
   ```

3. **Restart deployment for sidecar injection**
   ```bash
   kubectl rollout restart deployment/ilab-client -n ilab-chat
   ```

4. **Verify deployment**
   ```bash
   kubectl get pods -n ilab-chat
   kubectl get gateway,virtualservice -n ilab-chat
   ```

#### Accessing via Istio Ingress

**Get ingress details:**
```bash
# Get external IP
export INGRESS_HOST=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
export INGRESS_PORT=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.spec.ports[?(@.name=="http2")].port}')

# Access application
curl -H "Host: your-domain.com" http://$INGRESS_HOST:$INGRESS_PORT/ilabchat
```

**For NodePort setups:**
```bash
export INGRESS_HOST=$(kubectl get po -l istio=ingressgateway -n istio-system -o jsonpath='{.items[0].status.hostIP}')
export INGRESS_PORT=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.spec.ports[?(@.name=="http2")].nodePort}')

echo "Application available at: http://$INGRESS_HOST:$INGRESS_PORT/ilabchat"
```

## 🛠️ Development

### Local Development Setup

```bash
# Clone repository
git clone https://github.com/rafaelvzago/ilab-client.git
cd ilab-client

# Setup environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Start development server
export FLASK_ENV=development
export FLASK_DEBUG=True
python app.py
```

### Testing

```bash
# Test API endpoint
curl -X POST http://localhost:5000/api/completions \
  -H "Content-Type: application/json" \
  -d '{"question": "Test question"}'

# Test web interface
open http://localhost:5000
```

### Building Images

```bash
# Build with Docker
docker build -t ilab-client .

# Build with Podman
podman build -t ilab-client .

# Build with Make
make build
```

## 🔍 Troubleshooting

### Common Issues

#### Application Won't Start

**Problem**: `ModuleNotFoundError: No module named 'flask'`
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

**Problem**: `Address already in use`
```bash
# Solution: Check if port 5000 is in use
lsof -i :5000
# Kill process or change port
export FLASK_RUN_PORT=5001
```

#### API Connection Issues

**Problem**: `Connection refused to AI service`
```bash
# Solution: Verify AI service is running and ADDRESS is correct
curl -v $ADDRESS/v1/completions
export ADDRESS="http://correct-ai-service:8000"
```

#### Container Issues

**Problem**: Container exits immediately
```bash
# Solution: Check logs
docker logs ilab-client
podman logs ilab-client

# Common fix: Ensure ADDRESS environment variable is set
docker run -e ADDRESS="http://ai-service:8000" ilab-client
```

#### Kubernetes Issues

**Problem**: Pods in CrashLoopBackOff
```bash
# Solution: Check pod logs and events
kubectl logs deployment/ilab-client -n ilab-chat
kubectl describe pod -l app=ilab-client -n ilab-chat

# Check if ADDRESS is configured correctly
kubectl get deployment ilab-client -o yaml -n ilab-chat
```

#### Istio Issues

**Problem**: Traffic not routing through Istio
```bash
# Solution: Verify sidecar injection
kubectl get pods -n ilab-chat -o jsonpath='{.items[*].spec.containers[*].name}'
# Should show: ilab-client istio-proxy

# Check Istio configuration
kubectl get gateway,virtualservice -n ilab-chat
istioctl proxy-config cluster <pod-name> -n ilab-chat
```

### Debug Commands

```bash
# Check application status
kubectl get all -n ilab-chat

# View application logs
kubectl logs -f deployment/ilab-client -n ilab-chat

# Test internal connectivity
kubectl run debug --rm -it --image=curlimages/curl -- sh
# Inside pod: curl http://ilab-client-service.ilab-chat.svc.cluster.local:5000

# Check Istio sidecar status
istioctl proxy-status

# Analyze Istio configuration
istioctl analyze -n ilab-chat
```

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

### Development Process

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make changes and test**
4. **Follow commit conventions**
   ```bash
   git commit -m "feat: add new feature"
   git commit -m "fix: resolve bug in API"
   git commit -m "docs: update README"
   ```
5. **Submit a pull request**

### Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add comments for complex logic
- Include docstrings for functions and classes

### Testing

```bash
# Test the application before submitting
python app.py
curl -X POST http://localhost:5000/api/completions \
  -H "Content-Type: application/json" \
  -d '{"question": "Test"}'
```

## 📄 License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

---

**Maintainer**: Rafael Zago  
**Repository**: https://github.com/rafaelvzago/ilab-client  
**Issues**: https://github.com/rafaelvzago/ilab-client/issues