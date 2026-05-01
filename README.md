# 小米MiMo大模型 Web应用Demo

基于小米MiMo大模型API构建的智能对话Web应用，展示MiMo模型在推理、数学和代码任务中的能力。

## 项目简介

本项目是一个完整的Web应用Demo，用于申请小米MiMo大模型API免费token计划。项目展示了以下能力：

- **智能对话**: 调用MiMo大模型API进行多轮对话
- **推理能力**: 展示模型在逻辑推理和数学问题上的表现
- **代码生成**: 展示模型的代码理解和生成能力
- **Token统计**: 实时显示API调用的token消耗情况

## 技术栈

- **后端**: Python + Flask
- **前端**: 原生HTML/CSS/JavaScript
- **API**: 小米MiMo大模型API (OpenAI兼容格式)
- **部署**: 支持本地运行和云服务器部署

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置API

复制 `.env.example` 为 `.env` 并填入你的API配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件：
```env
MIMO_API_KEY=your-api-key-here
MIMO_BASE_URL=https://api.xiaomimimo.com/v1
MIMO_MODEL=MiMo-7B-RL
```

### 3. 运行应用

```bash
python app.py
```

访问 http://localhost:5000 即可使用。

## 应用场景

1. **智能客服**: 为用户提供24小时在线的智能问答服务
2. **学习助手**: 帮助学生解答数学、物理等学科问题
3. **编程辅助**: 协助开发者进行代码编写和调试
4. **内容创作**: 辅助进行文章撰写和创意生成

## 项目结构

```
xiaomi-mimo-demo/
├── app.py              # Flask后端主程序
├── templates/
│   └── index.html      # 前端界面
├── requirements.txt    # Python依赖
├── .env.example        # 环境变量模板
├── .gitignore          # Git忽略文件
└── README.md           # 项目说明
```

## API接口说明

### POST /api/chat
发送消息并获取AI回复

**请求参数:**
```json
{
    "message": "用户消息",
    "history": [{"role": "user/assistant", "content": "历史消息"}]
}
```

**响应:**
```json
{
    "response": "AI回复内容",
    "model": "使用的模型名称",
    "usage": {
        "prompt_tokens": 100,
        "completion_tokens": 50,
        "total_tokens": 150
    }
}
```

### GET /api/models
获取可用模型列表

## 申请说明

本项目用于申请小米MiMo大模型API免费token计划，主要展示：

1. **实际应用场景**: 智能对话助手在教育、客服、编程等领域的应用
2. **技术实现能力**: 完整的前后端开发和API集成能力
3. **用户体验设计**: 简洁美观的界面设计和流畅的交互体验
4. **扩展性**: 易于扩展和定制的架构设计

## 许可证

MIT License
