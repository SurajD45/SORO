from transformers import pipeline

# Load AI Chatbot
chatbot = pipeline("text-generation", model="microsoft/DialoGPT-medium")

def get_response(text):
    response = chatbot(text, max_length=100)
    return response[0]["generated_text"]