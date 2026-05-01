import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# 小米MiMo API配置
client = OpenAI(
    api_key=os.getenv("MIMO_API_KEY", "your-api-key-here"),
    base_url=os.getenv("MIMO_BASE_URL", "https://api.xiaomimimo.com/v1")
)

MODEL_NAME = os.getenv("MIMO_MODEL", "MiMo-7B-RL")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    history = data.get("history", [])

    if not user_message:
        return jsonify({"error": "消息不能为空"}), 400

    messages = [{"role": "system", "content": "你是小米MiMo大模型AI助手，擅长推理、数学和代码任务。请用中文回答用户的问题。"}]
    messages.extend(history)
    messages.append({"role": "user", "content": user_message})

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=0.7,
            max_tokens=2048,
            stream=False
        )
        assistant_message = response.choices[0].message.content
        return jsonify({
            "response": assistant_message,
            "model": MODEL_NAME,
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/models", methods=["GET"])
def list_models():
    try:
        models = client.models.list()
        return jsonify({"models": [m.id for m in models.data]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
