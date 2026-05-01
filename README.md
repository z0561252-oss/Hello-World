# MiMo Chat

一个基于大语言模型的智能对话Web应用，支持多轮对话、流式响应和实时性能统计。

## 功能特性

- **多轮对话** - 支持上下文感知的连续对话
- **流式响应** - 实时输出AI回复（SSE）
- **对话管理** - 创建、查看、删除对话历史
- **性能监控** - 实时显示Token消耗、响应速度
- **参数配置** - 可调节温度、最大Token数等参数
- **响应式设计** - 适配桌面和移动端
- **Docker支持** - 一键容器化部署

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端 | Python 3.11+, Flask |
| 前端 | 原生HTML/CSS/JavaScript |
| API | OpenAI兼容格式 |
| 部署 | Docker, Gunicorn |

## 快速开始

### 方式一：本地运行

```bash
# 克隆项目
git clone https://github.com/z0561252-oss/Hello-World.git
cd Hello-World

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 填入你的API配置

# 运行
python app.py
```

访问 http://localhost:5000

### 方式二：Docker部署

```bash
# 构建并运行
docker-compose up -d

# 查看日志
docker-compose logs -f
```

## 配置说明

在 `.env` 文件中配置以下参数：

| 参数 | 说明 | 默认值 |
|------|------|--------|
| MIMO_API_KEY | API密钥 | - |
| MIMO_BASE_URL | API地址 | https://api.xiaomimimo.com/v1 |
| MIMO_MODEL | 模型名称 | MiMo-7B-RL |
| TEMPERATURE | 生成温度 | 0.7 |
| MAX_TOKENS | 最大Token数 | 2048 |
| MAX_HISTORY | 历史消息数 | 20 |
| PORT | 服务端口 | 5000 |

## API文档

### POST /api/chat

发送消息并获取回复。

**请求：**
```json
{
    "message": "你好",
    "conversation_id": "optional-uuid"
}
```

**响应：**
```json
{
    "response": "你好！有什么可以帮助你的吗？",
    "model": "MiMo-7B-RL",
    "conversation_id": "uuid",
    "usage": {
        "prompt_tokens": 10,
        "completion_tokens": 15,
        "total_tokens": 25
    },
    "performance": {
        "elapsed_seconds": 0.5,
        "tokens_per_second": 30.0
    }
}
```

### POST /api/chat/stream

流式响应接口（SSE）。

### GET /api/conversations

获取对话列表。

### GET /api/conversations/{id}

获取指定对话的历史消息。

### DELETE /api/conversations/{id}

删除指定对话。

### GET /api/models

获取可用模型列表。

### GET /api/config

获取当前配置。

## 运行测试

```bash
pytest tests/ -v
```

## 项目结构

```
├── app.py                    # Flask后端
├── templates/
│   └── index.html            # 前端界面
├── tests/
│   └── test_app.py           # 单元测试
├── .github/
│   └── ISSUE_TEMPLATE/       # Issue模板
├── requirements.txt          # Python依赖
├── Dockerfile                # Docker配置
├── docker-compose.yml        # Docker Compose配置
├── .env.example              # 环境变量模板
├── .gitignore
├── LICENSE
└── README.md
```

## License

MIT
