# Media-Insight
### Use case 1: Text-to-Image Generation
### Use case 2: Image Captioin Generation
### Use case 3: Text Summarization (Extractive and Abstractive Summarization)


# How to start
All of the services are containerized now.

Install Docker: [Docker.com](https://www.docker.com/)

## Start the services (Please make sure ports 3000 is available)

```sh
docker compose up -d
```


# Usage

## frontend runs on http://localhost:3000
visit http://localhost:3000 for the ui


# Test
This command will execute all Python files starting with 'test' and all functions starting with 'test_' located under the backend/app/tests directory.
```sh
docker-compose -f docker-compose.test.yml up --build test
```

# Model Architecture

![WhatsApp Image 2024-11-21 at 17 47 24_281a0338](https://github.com/user-attachments/assets/a24dc39a-049a-4161-912f-ed8b7efddfd2)

# Updated Model Architecture

![model_docker_logs](https://github.com/user-attachments/assets/30cf2abe-e7db-4055-b4b1-3985d1b2c2b8)


# Data pipeline
![mlops-project-data-pipeline drawio](https://github.com/user-attachments/assets/7bccfa61-6941-435b-b7ab-3010cc86a469)

# A complete Architecture
![project-full-architecture](https://github.com/user-attachments/assets/69b7c6ba-1325-41e6-adca-1230c5254035)
