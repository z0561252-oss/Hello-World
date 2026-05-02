# MiMo Chat - 智能对话助手

一个基于大语言模型的智能对话Web应用，支持多轮对话、流式响应、Markdown渲染和实时性能监控。

## 项目简介

MiMo Chat 是一个功能完整的AI对话应用，旨在为用户提供流畅、智能的对话体验。项目采用前后端分离架构，后端基于Python Flask框架，前端使用原生HTML/CSS/JavaScript实现，通过OpenAI兼容格式接入大语言模型API。

### 核心能力

- **智能对话** - 支持上下文感知的多轮对话，AI能够理解前后文语义
- **流式响应** - 基于SSE（Server-Sent Events）实现打字机效果，实时输出AI回复
- **Markdown渲染** - 完整支持代码高亮、列表、引用等Markdown格式
- **对话管理** - 创建、查看、删除对话历史，支持多会话并行
- **性能监控** - 实时显示Token消耗、响应速度、耗时等指标
- **参数可调** - 支持调节温度、最大Token数、系统提示词等参数
- **响应式设计** - 自适应桌面和移动端，提供一致的用户体验

### 应用场景

| 场景 | 说明 |
|------|------|
| 智能客服 | 为用户提供7x24小时在线的智能问答服务 |
| 学习辅导 | 帮助学生解答数学、物理、编程等学科问题 |
| 编程辅助 | 协助开发者进行代码编写、调试和优化 |
| 内容创作 | 辅助进行文案撰写、创意生成和文本润色 |
| 知识问答 | 快速获取各类知识点的解释和说明 |

## 技术架构

```
┌─────────────────────────────────────────────────────────┐
│                      用户浏览器                          │
│  ┌───────────────────────────────────────────────────┐  │
│  │  前端界面 (HTML/CSS/JavaScript)                    │  │
│  │  - 对话交互    - Markdown渲染    - 设置面板        │  │
│  └───────────────────────┬───────────────────────────┘  │
└──────────────────────────┼──────────────────────────────┘
                           │ HTTP / SSE
┌──────────────────────────┼──────────────────────────────┐
│                    Flask 后端服务                        │
│  ┌───────────────────────┴───────────────────────────┐  │
│  │  API路由层                                         │  │
│  │  - /api/chat          - /api/chat/stream          │  │
│  │  - /api/conversations - /api/models               │  │
│  └───────────────────────┬───────────────────────────┘  │
│  ┌───────────────────────┴───────────────────────────┐  │
│  │  业务逻辑层                                        │  │
│  │  - 对话管理    - 消息处理    - 性能统计            │  │
│  └───────────────────────┬───────────────────────────┘  │
└──────────────────────────┼──────────────────────────────┘
                           │ OpenAI兼容格式
┌──────────────────────────┼──────────────────────────────┐
│              大语言模型 API 服务                         │
│  ┌───────────────────────┴───────────────────────────┐  │
│  │  MiMo / GPT / Claude / 其他兼容模型               │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### 技术栈

| 层级 | 技术 | 说明 |
|------|------|------|
| 后端框架 | Flask 3.x | 轻量级Python Web框架 |
| API客户端 | OpenAI SDK 1.x | 兼容OpenAI格式的API调用 |
| 前端 | 原生HTML/CSS/JavaScript | 零依赖，加载速度快 |
| Markdown | marked.js | 轻量级Markdown解析器 |
| 容器化 | Docker + Gunicorn | 生产级部署方案 |
| 测试 | pytest | 单元测试框架 |

## 快速开始

### 前置条件

- Python 3.10+
- 有效的API密钥（支持任何OpenAI兼容格式的API服务）

### 方式一：本地运行

```bash
# 1. 克隆项目
git clone https://github.com/z0561252-oss/Hello-World.git
cd Hello-World

# 2. 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入你的API配置

# 5. 运行应用
python app.py
```

访问 http://localhost:5000 即可使用。

### 方式二：Docker部署

```bash
# 1. 配置环境变量
cp .env.example .env
# 编辑 .env 文件

# 2. 构建并运行
docker-compose up -d

# 3. 查看日志
docker-compose logs -f

# 4. 停止服务
docker-compose down
```

## 配置说明

在 `.env` 文件中配置以下参数：

| 参数 | 必填 | 说明 | 默认值 |
|------|------|------|--------|
| `MIMO_API_KEY` | 是 | API密钥 | - |
| `MIMO_BASE_URL` | 否 | API接口地址 | `https://api.xiaomimimo.com/v1` |
| `MIMO_MODEL` | 否 | 模型名称 | `MiMo-7B-RL` |
| `TEMPERATURE` | 否 | 生成温度（0-2） | `0.7` |
| `MAX_TOKENS` | 否 | 单次回复最大Token数 | `2048` |
| `MAX_HISTORY` | 否 | 上下文历史消息数 | `20` |
| `SYSTEM_PROMPT` | 否 | 系统提示词 | 见文件 |
| `PORT` | 否 | 服务端口 | `5000` |
| `DEBUG` | 否 | 调试模式 | `false` |
| `SECRET_KEY` | 否 | Flask会话密钥 | 自动生成 |

## API文档

### POST /api/chat

发送消息并获取AI回复（非流式）。

**请求体：**
```json
{
    "message": "你好",
    "conversation_id": "可选的对话ID"
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

流式响应接口（SSE），实时输出AI回复。

**请求体：** 同 `/api/chat`

**响应格式：** Server-Sent Events
```
data: {"content": "你", "done": false}
data: {"content": "好", "done": false}
data: {"content": "", "done": true, "conversation_id": "uuid", "elapsed": 0.5}
```

### GET /api/conversations

获取所有对话列表。

**响应：**
```json
{
    "conversations": [
        {
            "id": "uuid",
            "title": "对话标题",
            "message_count": 4,
            "last_message": "最后一条消息预览"
        }
    ]
}
```

### GET /api/conversations/{id}

获取指定对话的完整历史消息。

### DELETE /api/conversations/{id}

删除指定对话。

### GET /api/models

获取可用模型列表。

### GET /api/config

获取当前服务配置。

## 项目结构

```
├── app.py                    # Flask后端主程序
├── templates/
│   └── index.html            # 前端界面（单页应用）
├── tests/
│   ├── __init__.py
│   └── test_app.py           # 单元测试
├── .github/
│   └── ISSUE_TEMPLATE/       # GitHub Issue模板
│       ├── bug_report.md     # Bug报告模板
│       └── feature_request.md # 功能建议模板
├── requirements.txt          # 生产依赖
├── requirements-dev.txt      # 开发依赖（含测试）
├── Dockerfile                # Docker镜像配置
├── docker-compose.yml        # Docker Compose配置
├── .dockerignore             # Docker构建忽略文件
├── .env.example              # 环境变量模板
├── .gitignore                # Git忽略文件
├── LICENSE                   # MIT开源许可证
└── README.md                 # 项目说明文档
```

## 开发指南

### 运行测试

```bash
# 安装开发依赖
pip install -r requirements-dev.txt

# 运行测试
pytest tests/ -v

# 运行测试并生成覆盖率报告
pytest tests/ -v --cov=app --cov-report=html
```

### 本地开发（热重载）

```bash
# 设置调试模式
export DEBUG=true

# 运行应用
python app.py
```

Flask会自动监听文件变化并重新加载。

## 部署建议

### 生产环境配置

1. **设置强密码** - 生成随机的 `SECRET_KEY`
2. **关闭调试** - 确保 `DEBUG=false`
3. **使用Gunicorn** - 已在Dockerfile中配置
4. **配置反向代理** - 推荐使用Nginx作为反向代理
5. **启用HTTPS** - 使用Let's Encrypt等免费SSL证书
6. **数据持久化** - 生产环境建议使用Redis或数据库存储对话历史

### Nginx配置示例

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # SSE支持
        proxy_buffering off;
        proxy_cache off;
        proxy_read_timeout 300s;
    }
}
```

## 常见问题

**Q: 如何更换其他AI模型？**

修改 `.env` 文件中的 `MIMO_BASE_URL` 和 `MIMO_MODEL` 即可。任何兼容OpenAI格式的API都可以使用。

**Q: 对话历史保存在哪里？**

当前版本使用内存存储，服务重启后会丢失。生产环境建议接入Redis或数据库。

**Q: 支持上传文件或图片吗？**

当前版本仅支持文本对话。图片和文件上传功能在开发计划中。

## License

[MIT](LICENSE)
