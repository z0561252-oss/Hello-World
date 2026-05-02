import json
import pytest
from unittest.mock import patch, MagicMock
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
    """测试空消息返回400"""
    response = client.post('/api/chat', json={'message': ''})
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data


def test_chat_whitespace_message(client):
    """测试空白消息返回400"""
    response = client.post('/api/chat', json={'message': '   '})
    assert response.status_code == 400


def test_chat_too_long_message(client):
    """测试超长消息返回400"""
    response = client.post('/api/chat', json={'message': 'x' * 10001})
    assert response.status_code == 400
    data = json.loads(response.data)
    assert '过长' in data['error']


@patch('app.client')
def test_chat_success(mock_client, client):
    """测试正常聊天请求"""
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "你好！"
    mock_response.usage.prompt_tokens = 10
    mock_response.usage.completion_tokens = 5
    mock_response.usage.total_tokens = 15
    mock_client.chat.completions.create.return_value = mock_response

    response = client.post('/api/chat', json={'message': '你好'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['response'] == "你好！"
    assert data['usage']['total_tokens'] == 15


@patch('app.client')
def test_chat_api_error(mock_client, client):
    """测试API错误处理"""
    mock_client.chat.completions.create.side_effect = Exception("API连接失败")

    response = client.post('/api/chat', json={'message': '你好'})
    assert response.status_code == 500
    data = json.loads(response.data)
    assert 'API连接失败' in data['error']


def test_config(client):
    """测试配置接口"""
    response = client.get('/api/config')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'model' in data
    assert 'temperature' in data
    assert 'max_tokens' in data


def test_conversations_empty(client):
    """测试空对话列表"""
    response = client.get('/api/conversations')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'conversations' in data
    assert data['conversations'] == []


def test_conversation_not_found(client):
    """测试获取不存在的对话"""
    response = client.get('/api/conversations/nonexistent')
    assert response.status_code == 404


def test_delete_conversation_not_found(client):
    """测试删除不存在的对话"""
    response = client.delete('/api/conversations/nonexistent')
    assert response.status_code == 404


@patch('app.client')
def test_list_models(mock_client, client):
    """测试模型列表接口"""
    mock_model = MagicMock()
    mock_model.id = "MiMo-7B-RL"
    mock_models = MagicMock()
    mock_models.data = [mock_model]
    mock_client.models.list.return_value = mock_models

    response = client.get('/api/models')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'models' in data
    assert 'MiMo-7B-RL' in data['models']


@patch('app.client')
def test_stream_chat(mock_client, client):
    """测试流式聊天接口"""
    mock_chunk1 = MagicMock()
    mock_chunk1.choices = [MagicMock()]
    mock_chunk1.choices[0].delta = MagicMock()
    mock_chunk1.choices[0].delta.content = "你"

    mock_chunk2 = MagicMock()
    mock_chunk2.choices = [MagicMock()]
    mock_chunk2.choices[0].delta = MagicMock()
    mock_chunk2.choices[0].delta.content = "好"

    mock_chunk3 = MagicMock()
    mock_chunk3.choices = [MagicMock()]
    mock_chunk3.choices[0].delta = MagicMock()
    mock_chunk3.choices[0].delta.content = None

    mock_client.chat.completions.create.return_value = iter([mock_chunk1, mock_chunk2, mock_chunk3])

    response = client.post('/api/chat/stream', json={'message': '你好'})
    assert response.status_code == 200
    assert response.content_type == 'text/event-stream'
