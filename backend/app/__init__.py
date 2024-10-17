import logging
from flask import Flask, request, redirect, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS



def create_app():
    app = Flask(__name__)
    cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
    api = Api(app, prefix='/api/v1')
    from app.main import rest_resources
    api.add_resource(rest_resources.Text2Image, '/generate-image', '/generate-image/<id>')
    api.add_resource(rest_resources.GenerateDescription, '/generate-description', '/generate-description/<id>')
    api.add_resource(rest_resources.GenerateText, '/summarize-text', '/summarize-text/<id>')

    return app
