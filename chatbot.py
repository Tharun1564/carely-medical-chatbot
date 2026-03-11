from flask import Flask, render_template, request
import openai
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Set OpenAI API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.form['message']
    response = get_medical_response(user_message)
    return render_template('index.html', user_message=user_message, response=response)

@app.route('/api/chat', methods=['POST'])
def api_chat():
    data = request.get_json()
    user_message = data.get('message', '')
    response = get_medical_response(user_message)
    return {'response': response}

def get_medical_response(message):
    if not openai.api_key:
        return "API key not configured. Please set OPENAI_API_KEY environment variable. For testing, you can get a free API key from https://platform.openai.com/"
    
    try:
        prompt = f"""You are a medical chatbot providing general health advice with specific treatment recommendations.
        IMPORTANT: Always emphasize that this is not a substitute for professional medical advice and users should consult healthcare professionals for personalized treatment.
        
        User query: {message}
        
        Provide helpful, specific advice for common symptoms including:
        - Common over-the-counter medications/tablets that may help
        - General treatment approaches
        - When to seek immediate medical attention
        - Home remedies and lifestyle changes
        
        Be direct and informative about treatment options while maintaining safety disclaimers. If the query is not medical, politely redirect to medical topics."""
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a knowledgeable medical assistant chatbot that provides specific treatment information including medication recommendations while emphasizing professional consultation."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.3
        )
        
        return response.choices[0].message.content.strip()
    except openai.AuthenticationError:
        return "Authentication failed. Please check your OpenAI API key is correct and has sufficient credits."
    except openai.RateLimitError:
        return "Rate limit exceeded. Please wait a moment before trying again, or check your OpenAI usage limits."
    except openai.APIError as e:
        return f"OpenAI API error: {str(e)}. Please try again later."
    except Exception as e:
        # Fallback to basic keyword responses if API fails
        return get_fallback_response(message)

def get_fallback_response(message):
    """Fallback keyword-based responses when API is unavailable"""
    message = message.lower()
    if 'headache' in message:
        return "For headaches, try over-the-counter pain relievers like acetaminophen (Tylenol) 500mg every 6 hours, or ibuprofen (Advil) 400mg. Rest in a quiet, dark room and stay hydrated. Consult a doctor if headaches persist or worsen."
    elif 'fever' in message:
        return "For fever, take acetaminophen (Tylenol) 500mg every 4-6 hours as needed. Stay hydrated and rest. Seek medical attention if fever exceeds 103°F (39.4°C) or lasts more than 3 days."
    elif 'cough' in message:
        return "For cough, try over-the-counter cough syrups containing dextromethorphan or guaifenesin. Drink warm fluids and use a humidifier. Consult a doctor if cough persists over 2 weeks or is accompanied by other symptoms."
    elif 'cold' in message:
        return "For common cold, rest, drink plenty of fluids, and use over-the-counter medications like acetaminophen for pain/fever and decongestants if needed. Symptoms usually resolve in 7-10 days. See a doctor if symptoms worsen."
    elif 'stomach pain' in message or 'abdominal pain' in message:
        return "For stomach pain, avoid heavy or spicy foods. Try ginger tea or over-the-counter antacids like Tums. If pain is severe or persistent, seek immediate medical attention."
    elif 'pain' in message:
        return "For general pain, consider over-the-counter options like acetaminophen (Tylenol) or ibuprofen (Advil/Motrin). Follow dosage instructions and consult a healthcare professional for persistent pain."
    elif 'infection' in message:
        return "For suspected infections, consult a healthcare professional for proper diagnosis and treatment. They may prescribe antibiotics if bacterial infection is confirmed."
    else:
        return "I'm currently experiencing technical difficulties with AI responses. For general medical advice, please consult a healthcare professional. What specific symptom are you experiencing? I can provide basic information about common conditions."

if __name__ == '__main__':
    app.run(debug=True)
