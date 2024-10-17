# Media-Insight
Use case 1: Text-to-Image Generation​

# add a DNS record in /etc/hosts
```sh
sudo echo "127.0.0.1    kafka_mediainsight" >> /etc/hosts
```

# db and message queue
Install Docker: [Docker.com](https://www.docker.com/)
```sh
cd backend
docker compose up -d
```

# frontend
```sh
cd frontend/mediainsight_ui
npm install
npm start
```

# backend api server
```sh
cd backend
pip install -r requirements.txt
pip install -U diffusers accelerate transformers -q
flask run
```

# backend consumer (consume kafka message and run ml task)
```sh
python run_consumer.py
```


# frontend running on http://localhost:3000
visit http://localhost:3000 for the ui


# backend api endpoint
DEBUG mode, localhost on port 5000
Running on http://127.0.0.1:5000

e.x.
# creating the text-to-image task
`curl -X POST http://127.0.0.1:5000/api/v1/generate-image`
# getting the task result
`curl -X GET http://127.0.0.1:5000/api/v1/generate-image/${task_id}`

