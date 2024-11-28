import pytest
from app import create_app
from mongomock import MongoClient
from bson.objectid import ObjectId 

@pytest.fixture
def app():
    app = create_app()  
    return app

@pytest.fixture
def client(app):
    # Create a mock Flask client for testing
    return app.test_client()

@pytest.fixture
def mock_db(monkeypatch):
    # Create a mock MongoDB client and database
    mock_client = MongoClient()
    mock_db = mock_client['test_db']
    
    # Replace MongoClient with mock_db
    monkeypatch.setattr('app.db', mock_db)
 
    return mock_db

@pytest.fixture
def mock_kafka(monkeypatch):
    # Create a mock Kafka producer
    class MockProducer:
        def produce(self, topic, value, callback=None):
            if callback:
                callback(None, type('obj', (object,), {
                    'topic': lambda: topic,
                    'partition': lambda: 0
                }))
        def flush(self):
            pass
    
    def mock_producer(*args, **kwargs):
        return MockProducer()
    
    monkeypatch.setattr('confluent_kafka.Producer', mock_producer)
    return MockProducer()

@pytest.fixture(autouse=True)
def setup_test_env(mock_db, mock_kafka):
    # Automatically use these fixtures
    pass