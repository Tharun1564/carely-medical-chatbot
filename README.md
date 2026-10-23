# Medical Chatbot

A web-based conversational health-information chatbot built with Python (Flask), HTML, CSS, and a local Ollama model.

## Features

- Generates conversational responses locally with Ollama's `llama3.2:3b` model
- Keeps the latest conversation turns as context while the page remains open
- Real-time chat interface with automatic responses (no page reloads)
- Web interface with a clean, user-friendly design
- Typing indicators for better user experience
- Does not require an API key or paid API credits
- Shows clear errors if Ollama is not running or the model is missing
- Disclaimer: This is for educational purposes only. Always consult a healthcare professional for medical advice.

## Installation

1. Ensure Python is installed.
2. Install the required dependencies:
   ```
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```
3. Install [Ollama for Windows](https://ollama.com/download/windows).
4. Open PowerShell and download the local model:
   ```powershell
   ollama pull llama3.2:3b
   ```
   This downloads several gigabytes. It uses your computer's storage and processing power, but not OpenAI API credits.
5. Verify Ollama has the model:
   ```powershell
   ollama list
   ```
6. The app connects to Ollama at `http://127.0.0.1:11434`. Ollama usually runs in the background after installation. If it is not running, start it with `ollama serve` in a separate PowerShell window.

## Troubleshooting

### Common Issues

**"Could not connect to Ollama"**
- Open the Ollama app or run `ollama serve` in another PowerShell window.

**"Ollama could not find model"**
- Run `ollama pull llama3.2:3b` and wait for the download to complete.

## Running the Application

1. Make sure Ollama is running and the model is downloaded.
2. In the project directory, activate the virtual environment and run the Flask application:
   ```
   python chatbot.py
   ```
3. Open your web browser and go to `http://127.0.0.1:5000`.

## Usage

- The chatbot greets you automatically
- Type your medical question or symptom description
- Press Enter or click "Send" for a locally generated AI response
- Responses use the recent conversation as context and appear without a page refresh
- Continue the conversation naturally

## Disclaimer

This chatbot is for general health education only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of a qualified health provider about medical conditions or treatment. Locally generated AI responses may be inaccurate and should not be used for emergencies or medication decisions.