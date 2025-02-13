from database import SessionLocal, DiaryEntry
from datetime import datetime

def add_diary_entry(user_id, text):
    db = SessionLocal()
    new_entry = DiaryEntry(user_id=user_id, entry=text, timestamp=datetime.utcnow())
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    db.close()
    return "Diary entry saved successfully!"

def get_user_mood(user_id):
    db = SessionLocal()
    entries = db.query(DiaryEntry).filter(DiaryEntry.user_id == user_id).all()
    db.close()
    
    # Analyze last 3 diary entries for mood detection
    if entries:
        mood_text = " ".join([entry.entry for entry in entries[-3:]])
        mood = analyze_sentiment(mood_text)
        return mood["compound"]
    return "No diary entries found."