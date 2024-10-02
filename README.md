# iLab Client

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)

A Flask web application that serves as a client interface for interacting with an AI language model API. It allows users to submit questions and receive generated responses.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Docker Deployment](#docker-deployment)
- [Contributing](#contributing)
- [License](#license)

## Features

- Simple web interface for interacting with an AI model.
- RESTful API endpoint for programmatic access.
- Docker support for containerized deployment.

## Prerequisites

- Python 3.10 or higher
- pip package manager
- Docker (optional, for container deployment)

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

## Docker Deployment

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

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
