from flask_restful import Resource
import random
from flask import request
from config import Config
from bson.objectid import ObjectId
from confluent_kafka import Producer
import json
from app import db


def save_to_mongodb(collection_name, data):
    collection = db[collection_name]
    result = collection.insert_one(data)
    return str(result.inserted_id)

def get_task_from_mongodb(collection_name, _id):
    collection = db[collection_name]
    result = collection.find_one({'_id': ObjectId(_id)})
    return result


def send_to_kafka(topic, message):
    topic_types = [Text2Image.kafka_topic, GenerateDescription.kafka_topic, GenerateText.kafka_topic]
    if topic not in topic_types:
        raise ValueError(f"Invalid topic type. Must be one of: {topic_types}")
    message['task_type'] = topic
    message = json.dumps(message).encode('utf-8')
    producer = Producer({'bootstrap.servers': Config.KAFKA_BOOTSTRAP_SERVERS})
    producer.produce(topic, message, callback=delivery_report)
    producer.flush()


def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))


class Text2Image(Resource):
    kafka_topic = 'text2image'
    collection_name = kafka_topic

    def get(self, id=None):
        ret = get_task_from_mongodb(self.collection_name, id)
        ret.pop('_id', None)
        if 'image' in ret:
            ret['image'] = f"http://localhost:5000/static/images/{ret['image']}"
        return {
            'task_id': id,
            'data': ret
        }

    def post(self):
        try:
            # get prompt text from request
            prompt_text = request.json['prompt_text']
            task_id = save_to_mongodb('text2image', {'text': prompt_text})
            # publish task to Kafka topic: text2image
            send_to_kafka(self.kafka_topic, {'task_id': task_id, 'prompt_text': prompt_text})
            return {'task_id': task_id}, 201
        except Exception as error:
            return {'error': str(error)}, 400


class GenerateDescription(Resource):
    kafka_topic = 'generate-description'
    collection_name = kafka_topic

    def get(self, id=None):
        return {
            'task_id': id,
        }
    
    def post(self):
        try:
            return {'task_id': random.randint(1, 10)}, 201
        except Exception as error:
            return {'error': str(error)}, 400


class GenerateText(Resource):
    kafka_topic = 'generate-text'
    collection_name = kafka_topic

    def get(self, id=None):
        return {'task_id': id }
    
    def post(self):
        try:
            return {'task_id': random.randint(1, 10)}, 201
        except Exception as error:
            return {'error': str(error)}, 400
