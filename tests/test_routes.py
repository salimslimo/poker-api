import pytest
import json
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.routes import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_start_game(client):
    response = client.post('/start', json={'num_players': 2})
    data = json.loads(response.data)
    assert response.status_code == 200
    assert 'game_id' in data