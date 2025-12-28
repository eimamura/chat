"""
Seed script to populate database with demo data.
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.database import SessionLocal, engine
from app.models.db_item import DBItem
from app.database import Base

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

# Seed data
seed_items = [
    "Sample Item 1",
    "Sample Item 2",
    "Sample Item 3",
    "Sample Item 4",
    "Sample Item 5",
]

def seed_database():
    """Seed the database with initial data."""
    db = SessionLocal()
    try:
        # Check if items already exist
        existing_count = db.query(DBItem).count()
        if existing_count > 0:
            print(f"Database already has {existing_count} items. Skipping seed.")
            return
        
        # Create seed items
        for name in seed_items:
            item = DBItem(name=name)
            db.add(item)
        
        db.commit()
        print(f"Successfully seeded {len(seed_items)} items.")
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()

