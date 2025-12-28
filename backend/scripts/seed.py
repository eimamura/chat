"""
Seed script to populate database with demo chat messages.
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.database import SessionLocal, engine
from app.models.db_message import DBMessage
from app.database import Base

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

# Seed data - sample chat messages
seed_messages = [
    ("Alice", "Hello! This is a chat MVP demo."),
    ("Bob", "Hi Alice! Nice to see you here."),
    ("Charlie", "Hey everyone! How's it going?"),
    ("Alice", "Great! This chat app is working well."),
    ("Bob", "Yes, it's a simple but functional MVP."),
]

def seed_database():
    """Seed the database with initial chat messages."""
    db = SessionLocal()
    try:
        # Check if messages already exist
        existing_count = db.query(DBMessage).count()
        if existing_count > 0:
            print(f"Database already has {existing_count} messages. Skipping seed.")
            return
        
        # Create seed messages
        for username, content in seed_messages:
            message = DBMessage(username=username, content=content)
            db.add(message)
        
        db.commit()
        print(f"Successfully seeded {len(seed_messages)} messages.")
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
