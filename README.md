# Media-Insight
Use case 1: Text-to-Image Generation


# How to start
most of the services are containerized now,
except for consumer and model, 
saving us the trouble to download large library again.

## 1. web, db and message queue
Install Docker: [Docker.com](https://www.docker.com/)
```sh
docker compose up -d
```

## 2. install gen ai library
```sh
cd backend
pip install -r requirements-genai.txt
```

## 3. backend consumer (consume kafka message and run ml task)
```sh
python run_consumer.py
```

# Usage

## frontend runs on http://localhost:3000
visit http://localhost:3000 for the ui


# backend api endpoint
DEBUG mode, localhost on port 5000
Running on http://127.0.0.1:5000

e.x.
# create the text-to-image task
```sh
curl --header "Content-Type: application/json" \
  -X POST \
  --data '{"text": "robot"}' \
  http://127.0.0.1:5000/api/v1/generate-image
```
# get the task result
```sh
curl -X GET http://127.0.0.1:5000/api/v1/generate-image/${task_id}
```

