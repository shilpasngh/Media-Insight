from flask import Flask, request, redirect, jsonify
from flask_restful import Resource, Api
# from flask_cors import CORS
import random


app = Flask(__name__)


# cors = CORS(app, resources={r"*": {"origins": "*"}})
api = Api(app, prefix='/api/v1')


class Text2Image(Resource):
    def get(self, id=None):
        return {
            'task_id': id,
            'url': 'http://localhost:5000/static/images/' + str(id)
        }

    def post(self):
        try:
            return {'task_id': random.randint(1, 10)}, 201
        except Exception as error:
            return {'error': error}


class GenerateDescription(Resource):
    def get(self, id=None):
        return {
            'task_id': id,
        }
    
    def post(self):
        try:
            return {'task_id': random.randint(1, 10)}, 201
        except Exception as error:
            return {'error': error}


class GenerateText(Resource):
    def get(self, id=None):
        return {'task_id': id }
    
    def post(self):
        try:
            return {'task_id': random.randint(1, 10)}, 201
        except Exception as error:
            return {'error': error}


api.add_resource(Text2Image, '/generate-image', '/generate-image/<int:id>')
api.add_resource(GenerateDescription, '/generate-description', '/generate-description/<int:id>')
api.add_resource(GenerateText, '/summarize-text', '/summarize-text/<int:id>')


if __name__ == '__main__':
    app.run(debug=True)
