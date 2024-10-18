# Media-Insight
Use case 1: Text-to-Image Generation​

# How to start

## 1. add a DNS record in /etc/hosts
```sh
sudo echo "127.0.0.1    kafka_mediainsight" >> /etc/hosts
```

## 2. db and message queue
Install Docker: [Docker.com](https://www.docker.com/)
```sh
cd backend
docker compose up -d
```

## 3. enter the Kafka container
```sh
docker exec --workdir /opt/bitnami/kafka/bin/ -it kafka_mediainsight sh
```

## 4. create a topic
```sh
./kafka-topics.sh --bootstrap-server :9092 --create --topic text2image
./kafka-topics.sh --bootstrap-server :9092 --create --topic generate-description
./kafka-topics.sh --bootstrap-server :9092 --create --topic generate-text
```

## 5. start frontend
```sh
cd frontend/mediainsight_ui
npm install
npm start
```

## 6. start backend api server
```sh
cd backend
pip install -r requirements.txt
pip install -U diffusers accelerate transformers -q
flask run
```

## 7. backend consumer (consume kafka message and run ml task)
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
  --data '{"prompt_text": "robot"}' \
  http://127.0.0.1:5000/api/v1/generate-image
```
# get the task result
```sh
curl -X GET http://127.0.0.1:5000/api/v1/generate-image/${task_id}
```

