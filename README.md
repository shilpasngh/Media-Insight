# Media-Insight
This is a branch for Use case 1: Text-to-Image Generation​

# frontend
```sh
cd frontend/mediainsight_ui
npm install
npm start
```

# backend
```sh
cd backend
pip install -r requirements.txt
python app.py
```


# backend api endpoint
DEBUG mode, localhost on port 5000
Running on http://127.0.0.1:5000

e.x.
# creating the text-to-image task
`curl -X POST http://127.0.0.1:5000/api/v1/generate-image`
# getting the task result
`curl -X GET http://127.0.0.1:5000/api/v1/generate-image/1`

