from app import create_app, db
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(basedir, '.env')
load_dotenv(path)
from app.main.kafka_consumer import kafka_consumer


app = create_app()



if __name__ == '__main__':
    kafka_consumer(db)