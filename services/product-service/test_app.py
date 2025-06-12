import json
import pytest
from unittest.mock import patch
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
    assert data['service'] == 'product-service'

def test_get_products(client):
    response = client.get('/products')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) > 0

def test_get_product(client):
    response = client.get('/products/1')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['id'] == 1
    assert 'name' in data
    assert 'price' in data

def test_product_not_found(client):
    response = client.get('/products/999')
    assert response.status_code == 404

def test_create_product(client):
    new_product = {
        'name': 'Test Product',
        'price': 19.99,
        'in_stock': True
    }
    response = client.post('/products', 
                          data=json.dumps(new_product),
                          content_type='application/json')
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['name'] == 'Test Product'
    assert data['price'] == 19.99
    assert data['in_stock'] is True
    assert 'id' in data

@patch('requests.get')
def test_get_user_products_success(mock_get, client):
    # Mock the user service response
    mock_response = type('Response', (), {
        'status_code': 200,
        'json': lambda: {"id": 1, "name": "John Doe", "email": "john@example.com"}
    })
    mock_get.return_value = mock_response
    
    response = client.get('/products/user/1')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'user' in data
    assert 'recommended_products' in data
    assert data['user']['id'] == 1

@patch('requests.get')
def test_get_user_products_user_not_found(mock_get, client):
    # Mock the user service response for user not found
    mock_response = type('Response', (), {
        'status_code': 404,
        'json': lambda: {"error": "User not found"}
    })
    mock_get.return_value = mock_response
    
    response = client.get('/products/user/999')
    assert response.status_code == 404

@patch('requests.get')
def test_get_user_products_service_error(mock_get, client):
    # Mock a service communication error
    mock_get.side_effect = Exception("Connection error")
    
    response = client.get('/products/user/1')
    assert response.status_code == 503
    data = json.loads(response.data)
    assert 'error' in data
