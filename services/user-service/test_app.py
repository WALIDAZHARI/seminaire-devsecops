import json
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'
    assert data['service'] == 'user-service'

def test_get_users(client):
    response = client.get('/users')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) > 0

def test_get_user(client):
    response = client.get('/users/1')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['id'] == 1
    assert 'name' in data
    assert 'email' in data

def test_user_not_found(client):
    response = client.get('/users/999')
    assert response.status_code == 404

def test_create_user(client):
    new_user = {
        'name': 'Test User',
        'email': 'test@example.com'
    }
    response = client.post('/users', 
                          data=json.dumps(new_user),
                          content_type='application/json')
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['name'] == 'Test User'
    assert data['email'] == 'test@example.com'
    assert 'id' in data
