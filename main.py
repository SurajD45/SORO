from fastapi import FastAPI, Depends
from pydantic import BaseModel
from chatbot import get_response
from sentiment_analysis import analyze_sentiment
from crisis_detection import detect_crisis
from voice_input import voice_to_text
from diary import add_diary_entry, get_user_mood
from database import SessionLocal, ChatHistory
from twilio.rest import Client
from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_NUMBER
from sqlalchemy.orm import Session

app = FastAPI()

# Twilio Client
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

class Message(BaseModel):
    text: str

@app.post("/chat")
def chat(msg: Message, db: Session = Depends(SessionLocal)):
    if detect_crisis(msg.text):
        response = "I'm really sorry you're feeling this way. Please seek immediate help or talk to a mental health professional."
        return {"response": response}

    sentiment = analyze_sentiment(msg.text)
    ai_response = get_response(msg.text)

    new_chat = ChatHistory(user_message=msg.text, chatbot_response=ai_response, sentiment=sentiment["compound"])
    db.add(new_chat)
    db.commit()

    return {"response": ai_response, "sentiment": sentiment}

@app.post("/diary")
def diary_entry(user_id: int, text: str):
    return add_diary_entry(user_id, text)

@app.get("/mood/{user_id}")
def mood_analysis(user_id: int):
    return get_user_mood(user_id)

@app.post("/voice-chat")
def voice_chat():
    text = voice_to_text()
    return chat(Message(text=text))

@app.post("/whatsapp")
def send_whatsapp(msg: Message, to: str):
    client.messages.create(
        body=msg.text,
        from_=TWILIO_WHATSAPP_NUMBER,
        to=f"whatsapp:{to}"
    )
    return {"message": "Sent successfully!"}