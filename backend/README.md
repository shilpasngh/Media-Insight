# install dependencies
```sh
pip install -r requirements.txt
```
```sh
pip install -U diffusers accelerate transformers -q
```

# run MongoDB and Kafka locally in docker
```sh
docker compose up -d
```

## enter the Kafka container
```sh
docker exec --workdir /opt/bitnami/kafka/bin/ -it kafka_mediainsight sh
```

## create a topic
```sh
./kafka-topics.sh --bootstrap-server :9092 --create --topic text2image
./kafka-topics.sh --bootstrap-server :9092 --create --topic generate-description
./kafka-topics.sh --bootstrap-server :9092 --create --topic generate-text
```
