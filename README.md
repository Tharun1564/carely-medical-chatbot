# Medical Chatbot

A simple web-based medical chatbot built with Python (Flask), HTML, CSS, and OpenAI API with real-time AJAX responses.

## Features

- Provides AI-generated medical advice using OpenAI's GPT model with specific treatment recommendations
- Includes information about common tablets/medications and treatment solutions
- Real-time chat interface with automatic responses (no page reloads)
- Web interface with a clean, user-friendly design
- Typing indicators for better user experience
- **Fallback System**: Automatically switches to reliable keyword-based responses if API fails
- Disclaimer: This is for educational purposes only. Always consult a healthcare professional for medical advice.

## Installation

1. Ensure you have Python installed (version 3.6 or higher).
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Get an OpenAI API key from [OpenAI](https://platform.openai.com/).
4. Set the API key as an environment variable:
   - On Windows: `set OPENAI_API_KEY=your_api_key_here`
   - On Windows (PowerShell): `$env:OPENAI_API_KEY="your_api_key_here"`
   - On Linux/Mac: `export OPENAI_API_KEY=your_api_key_here`

## Troubleshooting

### Common Issues

**"API key not configured"**
- Make sure you've set the OPENAI_API_KEY environment variable
- Verify the API key is correct and active

**"Authentication failed"**
- Check that your OpenAI API key is valid
- Ensure you have credits in your OpenAI account

**"Rate limit exceeded"**
- You've hit OpenAI's rate limits
- Wait a few minutes before trying again
- Consider upgrading your OpenAI plan for higher limits

**Fallback Mode**
- If API calls fail, the chatbot automatically switches to basic keyword-based responses
- You'll still get helpful medical information even without the AI

### Testing Without API Key

The chatbot includes fallback responses for common symptoms when the API is unavailable, so you can still test basic functionality.

## Running the Application

1. Navigate to the project directory.
2. Run the Flask application:
   ```
   python chatbot.py
   ```
3. Open your web browser and go to `http://127.0.0.1:5000`.

## Usage

- The chatbot greets you automatically
- Type your medical question or symptom description
- Press Enter or click "Send" for instant AI-generated responses with specific treatment recommendations
- Responses appear immediately without page refreshes and include information about tablets/medications when appropriate
- Continue the conversation naturally

## Disclaimer

This chatbot is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition. The AI responses are generated based on general knowledge and may not be accurate for individual cases.