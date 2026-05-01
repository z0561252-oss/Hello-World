import json
import pytest
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_index(client):
    """测试首页加载"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'MiMo Chat' in response.data


def test_chat_empty_message(client):
    """测试空消息"""
    response = client.post('/api/chat', json={'message': ''})
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data


def test_list_models(client):
    """测试模型列表接口"""
    response = client.get('/api/models')
    assert response.status_code == 200


def test_config(client):
    """测试配置接口"""
    response = client.get('/api/config')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'model' in data
    assert 'temperature' in data


def test_conversations(client):
    """测试对话列表接口"""
    response = client.get('/api/conversations')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'conversations' in data
