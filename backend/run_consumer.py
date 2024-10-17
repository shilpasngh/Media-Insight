from app import create_app
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(basedir, '.env')
load_dotenv(path)
from app.main.kafka_consumer import kafka_consumer
from config import Config
import pymongo

app = create_app()
client = pymongo.MongoClient(Config.MONGODB_URI)
db = client[Config.MONGODB_DB]


if __name__ == '__main__':
    kafka_consumer(db)