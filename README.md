# Media-Insight
This is a branch for Use case 1: Text-to-Image Generation​


# building the Flask app
The dependencies are saved in "requirements.txt"

`pip install -r requirements.txt` to install dependencies

# running the app
`python app.py` to run Flask app

# api endpoint
DEBUG mode, localhost on port 5000
Running on http://127.0.0.1:5000

e.x.
# creating the text-to-image task
`curl -X POST http://127.0.0.1:5000/api/v1/generate-image`
# getting the task result
`curl -X GET http://127.0.0.1:5000/api/v1/generate-image/1`

