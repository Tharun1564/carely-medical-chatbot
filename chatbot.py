from flask import Flask, jsonify, render_template, request
import json
import os
import socket
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

ollama_url = os.getenv('OLLAMA_URL', 'http://127.0.0.1:11434').rstrip('/')
ollama_model = os.getenv('OLLAMA_MODEL', 'llama3.2:3b')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.form.get('message', '').strip()
    try:
        response = get_medical_response(user_message)
    except AIServiceError as error:
        response = error.message
    return render_template('index.html', user_message=user_message, response=response)

@app.route('/api/chat', methods=['POST'])
def api_chat():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(error="Send a valid JSON request."), 400

    user_message = data.get('message')
    history = data.get('history', [])
    if not isinstance(user_message, str) or not user_message.strip():
        return jsonify(error="Enter a message before sending."), 400
    if len(user_message) > 4000:
        return jsonify(error="Please keep each message under 4,000 characters."), 400
    if not isinstance(history, list) or len(history) > 12:
        return jsonify(error="The conversation is too long. Start a new conversation and try again."), 400

    validated_history = []
    for item in history:
        if (
            not isinstance(item, dict)
            or item.get('role') not in ('user', 'assistant')
            or not isinstance(item.get('content'), str)
        ):
            return jsonify(error="The conversation history is invalid. Please refresh and try again."), 400
        validated_history.append({
            'role': item['role'],
            'content': item['content'][:4000],
        })

    try:
        answer = get_medical_response(user_message.strip(), validated_history)
        return jsonify(response=answer)
    except AIServiceError as error:
        return jsonify(error=error.message), error.status_code


class AIServiceError(Exception):
    def __init__(self, message, status_code):
        self.message = message
        self.status_code = status_code


def get_medical_response(message, history=None):
    messages = [
        {
            "role": "system",
            "content": (
                "You are a warm, attentive conversational assistant for general health education. "
                "Talk naturally and kindly, including when the user greets you or asks a non-medical "
                "small-talk question. For health questions, first acknowledge the concern, then explain "
                "what may be going on in clear everyday language, what safe next steps they can take, "
                "and which warning signs need urgent care. Ask relevant follow-up questions rather than "
                "guessing when key details are missing. Never claim to diagnose, never make up facts, "
                "and do not prescribe or invent medication doses. Encourage a clinician or pharmacist "
                "for personalized medical or medication advice. Be specific and useful, not formulaic, "
                "and avoid repeating disclaimers unless they matter to the current answer."
            ),
        },
    ]
    messages.extend(history or [])
    messages.append({"role": "user", "content": message})

    payload = json.dumps({
        "model": ollama_model,
        "messages": messages,
        "stream": False,
        "options": {"temperature": 0.6},
    }).encode("utf-8")
    request = Request(
        f"{ollama_url}/api/chat",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urlopen(request, timeout=180) as response:
            result = json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        details = error.read().decode("utf-8", errors="replace")
        print(f"Ollama request failed with HTTP {error.code}: {details}")
        if error.code == 404:
            raise AIServiceError(
                f"Ollama could not find model '{ollama_model}'. Run "
                f"`ollama pull {ollama_model}` in PowerShell.",
                503,
            ) from error
        raise AIServiceError(
            "Ollama returned an error. Check the Ollama app and the PowerShell output.",
            502,
        ) from error
    except (URLError, socket.timeout, TimeoutError) as error:
        print(f"Could not connect to Ollama at {ollama_url}: {error}")
        raise AIServiceError(
            "Could not connect to Ollama. Install and start Ollama, then try again.",
            503,
        ) from error
    except (json.JSONDecodeError, KeyError, TypeError) as error:
        print(f"Invalid response from Ollama: {error}")
        raise AIServiceError("Ollama returned an invalid response. Please try again.", 502) from error

    message_result = result.get("message") if isinstance(result, dict) else None
    answer = message_result.get("content") if isinstance(message_result, dict) else None
    if isinstance(answer, str) and answer.strip():
        return answer.strip()
    raise AIServiceError("Ollama returned an empty response. Please try again.", 502)

if __name__ == '__main__':
    app.run(debug=True)
