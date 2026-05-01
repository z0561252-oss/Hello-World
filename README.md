# MiMo Chat - 智能对话助手

一个基于大语言模型的智能对话Web应用，支持多轮对话、实时Token统计和优雅的交互体验。

## 功能特性

- **智能对话**: 支持上下文感知的多轮对话
- **实时统计**: 显示每次对话的Token消耗
- **响应式设计**: 适配桌面和移动端
- **简洁界面**: 现代化UI，流畅的交互体验

## 技术栈

- **后端**: Python + Flask
- **前端**: 原生HTML/CSS/JavaScript
- **API**: OpenAI兼容格式

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 配置API

复制 `.env.example` 为 `.env` 并填入配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你的API配置：
```env
MIMO_API_KEY=your-api-key-here
MIMO_BASE_URL=your-api-endpoint
MIMO_MODEL=your-model-name
```

### 运行

```bash
python app.py
```

访问 http://localhost:5000

## 项目结构

```
├── app.py              # Flask后端
├── templates/
│   └── index.html      # 前端界面
├── requirements.txt    # 依赖
├── .env.example        # 配置模板
└── README.md
```

## API接口

### POST /api/chat

发送消息获取回复。

**请求:**
```json
{
    "message": "你好",
    "history": []
}
```

**响应:**
```json
{
    "response": "你好！有什么可以帮助你的吗？",
    "model": "model-name",
    "usage": {
        "prompt_tokens": 10,
        "completion_tokens": 15,
        "total_tokens": 25
    }
}
```

## License

MIT
