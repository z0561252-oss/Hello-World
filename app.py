import os
import json
import time
import uuid
from datetime import datetime
from flask import Flask, render_template, request, jsonify, Response, session
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "mimo-chat-secret-key")

# API配置
client = OpenAI(
    api_key=os.getenv("MIMO_API_KEY", "your-api-key-here"),
    base_url=os.getenv("MIMO_BASE_URL", "https://api.xiaomimimo.com/v1")
)

MODEL_NAME = os.getenv("MIMO_MODEL", "MiMo-7B-RL")
MAX_HISTORY = int(os.getenv("MAX_HISTORY", "20"))

# 内存中的对话存储（生产环境应使用数据库）
conversations = {}


@app.route("/")
def index():
    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4())
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    conversation_id = data.get("conversation_id", session.get("session_id", "default"))

    if not user_message:
        return jsonify({"error": "消息不能为空"}), 400

    # 获取或创建对话历史
    if conversation_id not in conversations:
        conversations[conversation_id] = []

    history = conversations[conversation_id]

    messages = [{"role": "system", "content": get_system_prompt()}]
    messages.extend(history[-MAX_HISTORY:])
    messages.append({"role": "user", "content": user_message})

    try:
        start_time = time.time()
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=float(os.getenv("TEMPERATURE", "0.7")),
            max_tokens=int(os.getenv("MAX_TOKENS", "2048")),
            stream=False
        )
        elapsed = time.time() - start_time

        assistant_message = response.choices[0].message.content

        # 保存对话历史
        history.append({"role": "user", "content": user_message})
        history.append({"role": "assistant", "content": assistant_message})

        return jsonify({
            "response": assistant_message,
            "model": MODEL_NAME,
            "conversation_id": conversation_id,
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            },
            "performance": {
                "elapsed_seconds": round(elapsed, 2),
                "tokens_per_second": round(response.usage.completion_tokens / elapsed, 1) if elapsed > 0 else 0
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/chat/stream", methods=["POST"])
def chat_stream():
    data = request.get_json()
    user_message = data.get("message", "")
    conversation_id = data.get("conversation_id", session.get("session_id", "default"))

    if not user_message:
        return jsonify({"error": "消息不能为空"}), 400

    if conversation_id not in conversations:
        conversations[conversation_id] = []

    history = conversations[conversation_id]

    messages = [{"role": "system", "content": get_system_prompt()}]
    messages.extend(history[-MAX_HISTORY:])
    messages.append({"role": "user", "content": user_message})

    def generate():
        full_response = ""
        try:
            stream = client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                temperature=float(os.getenv("TEMPERATURE", "0.7")),
                max_tokens=int(os.getenv("MAX_TOKENS", "2048")),
                stream=True
            )

            for chunk in stream:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    full_response += content
                    yield f"data: {json.dumps({'content': content, 'done': False})}\n\n"

            # 保存对话历史
            history.append({"role": "user", "content": user_message})
            history.append({"role": "assistant", "content": full_response})

            yield f"data: {json.dumps({'content': '', 'done': True, 'conversation_id': conversation_id})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e), 'done': True})}\n\n"

    return Response(generate(), mimetype="text/event-stream")


@app.route("/api/conversations", methods=["GET"])
def list_conversations():
    result = []
    for conv_id, messages in conversations.items():
        if messages:
            result.append({
                "id": conv_id,
                "title": messages[0]["content"][:50] + "..." if len(messages[0]["content"]) > 50 else messages[0]["content"],
                "message_count": len(messages),
                "last_message": messages[-1]["content"][:100] if messages else ""
            })
    return jsonify({"conversations": result})


@app.route("/api/conversations/<conversation_id>", methods=["GET"])
def get_conversation(conversation_id):
    if conversation_id not in conversations:
        return jsonify({"error": "对话不存在"}), 404
    return jsonify({"messages": conversations[conversation_id]})


@app.route("/api/conversations/<conversation_id>", methods=["DELETE"])
def delete_conversation(conversation_id):
    if conversation_id in conversations:
        del conversations[conversation_id]
        return jsonify({"success": True})
    return jsonify({"error": "对话不存在"}), 404


@app.route("/api/models", methods=["GET"])
def list_models():
    try:
        models = client.models.list()
        return jsonify({"models": [m.id for m in models.data]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/config", methods=["GET"])
def get_config():
    return jsonify({
        "model": MODEL_NAME,
        "temperature": float(os.getenv("TEMPERATURE", "0.7")),
        "max_tokens": int(os.getenv("MAX_TOKENS", "2048")),
        "max_history": MAX_HISTORY
    })


def get_system_prompt():
    return os.getenv("SYSTEM_PROMPT", "你是一个智能AI助手，擅长推理、数学和代码任务。请用中文回答用户的问题。回答要简洁明了，逻辑清晰。")


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    debug = os.getenv("DEBUG", "true").lower() == "true"
    app.run(debug=debug, host="0.0.0.0", port=port)
