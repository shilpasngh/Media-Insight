import pytest
import json
from io import BytesIO

def test_summarize_text_post(client, mock_db):
    test_data = {
        "prompt": "Test prompt"
    }
    
    # Send POST request
    response = client.post(
        '/api/v1/summarize-text',
        json=test_data
    )
    
    # Verify response
    print(f"Response: {response.data}")
    assert response.status_code == 201
    assert 'task_id' in response.json

def test_summarize_text_get(client, mock_db):
    # Create a task
    test_data = {"prompt": "Test prompt"}
    post_response = client.post(
        '/api/v1/summarize-text',
        json=test_data
    )
    task_id = post_response.json['task_id']
    
    # Test GET request
    response = client.get(f'/api/v1/summarize-text/{task_id}')
    print(f"GET Response: {response.data}")
    assert response.status_code == 200
    assert 'data' in response.json