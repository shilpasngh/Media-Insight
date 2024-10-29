# Media-Insight
Use case 1: Text-to-Image Generation


# How to start
All of the services are containerized now.

Install Docker: [Docker.com](https://www.docker.com/)

## Start the services (Please make sure ports 3000, 5000, 8080, 9092, 27017 are available)

```sh
docker compose up -d
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

