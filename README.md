# iLab Client

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)

A Flask web application that serves as a client interface for interacting with an AI language model API. It allows users to submit questions and receive generated responses.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Docker/Podman Deployment](#dockerpodman-deployment)
- [Kubernetes Deployment](#kubernetes-deployment)
- [Contributing](#contributing)
- [License](#license)

## Features

- Simple web interface for interacting with an AI model.
- RESTful API endpoint for programmatic access.
- Docker/Podman support for containerized deployment.
- Kubernetes manifests for cluster deployment.

## Prerequisites

- Python 3.10 or higher
- pip package manager
- Docker or Podman (optional, for container deployment)
- Make (optional, for building with Makefile)

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/rafaelvzago/ilab-client.git
   cd ilab-client
   ```

2. **Create and activate a virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Set the `ADDRESS` environment variable to point to your AI language model API. By default, it uses `http://127.0.0.1:8000`.

```bash
export ADDRESS="http://api.your-aiservice.com"
```

## Usage

1. **Run the application**

   ```bash
   python app.py
   ```

2. **Access the web interface**

   Open your browser and navigate to `http://localhost:5000`.

3. **API Endpoint**

   - **URL**: `/api/completions`
   - **Method**: `POST`
   - **Headers**: `Content-Type: application/json`
   - **Body**:

     ```json
     {
       "question": "Your question here"
     }
     ```

   - **Response**:

     ```json
     {
       "response": "AI-generated response"
     }
     ```

## Docker/Podman Deployment

### Using Makefile (Recommended)

1. **Build the image locally**

   ```bash
   make build
   ```

2. **Build and tag with registry**

   ```bash
   make build-registry REGISTRY=quay.io/your-username IMAGE_TAG=latest
   ```

3. **Build and push to registry**

   ```bash
   make push REGISTRY=quay.io/your-username IMAGE_TAG=latest
   ```

4. **Clean up local images**

   ```bash
   make clean
   ```

5. **Run the container**

   ```bash
   podman run -d -p 5000:5000 --name ilab-client ilab-client:latest
   # or with registry image
   podman run -d -p 5000:5000 --name ilab-client quay.io/your-username/ilab-client:latest
   ```

### Manual Docker Commands

1. **Build the Docker image**

   ```bash
   docker build -t ilab-client .
   ```

2. **Run the Docker container**

   ```bash
   docker run -d -p 5000:5000 --name ilab-client ilab-client
   ```

3. **Set the `ADDRESS` environment variable**

   ```bash
   docker run -d -p 5000:5000 -e ADDRESS="http://api.your-aiservice.com" --name ilab-client ilab-client
   ```

### Manual Podman Commands

1. **Build the Podman image**

   ```bash
   podman build -t ilab-client .
   ```

2. **Run the Podman container**

   ```bash
   podman run -d -p 5000:5000 --name ilab-client ilab-client
   ```

## Kubernetes Deployment

The `manifests/` directory contains Kubernetes deployment files:

- `deployment.yaml` - Application deployment with resource limits and health checks
- `service.yaml` - LoadBalancer service for external access
- `route.yaml` - OpenShift route for ingress (if using OpenShift)

1. **Deploy to Kubernetes**

   ```bash
   kubectl apply -f manifests/
   ```

2. **Deploy to OpenShift**

   ```bash
   oc apply -f manifests/
   ```

3. **Update the AI service address**

   Edit `manifests/deployment.yaml` and modify the `ADDRESS` environment variable, then reapply:

   ```bash
   kubectl apply -f manifests/deployment.yaml
   ```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
