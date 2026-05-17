import os
import sys
import json
from dotenv import load_dotenv
import psycopg2
from pgvector.psycopg2 import register_vector

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

load_dotenv()

from app.embeddings import get_embedding

def seed_database():
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    register_vector(conn)
    cur = conn.cursor()

    # Enable extension
    cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")

    # === DROP EXISTING TABLE TO RECREATE WITH UNIQUE ===
    print("🗑️  Dropping old items table to add UNIQUE constraint...")
    cur.execute("DROP TABLE IF EXISTS items CASCADE;")

    # Create fresh table with UNIQUE title
    cur.execute("""
        CREATE TABLE items (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL UNIQUE,
            description TEXT,
            category TEXT NOT NULL,
            metadata JSONB,
            embedding VECTOR(384)
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_feedback (
            id SERIAL PRIMARY KEY,
            user_id TEXT,
            item_id INTEGER REFERENCES items(id),
            rating FLOAT,
            feedback_text TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # Vector index
    cur.execute("""
        CREATE INDEX IF NOT EXISTS items_embedding_idx 
        ON items USING hnsw (embedding vector_cosine_ops);
    """)

    conn.commit()
    print("✅ Tables recreated with UNIQUE constraint!")

    # Sample data
    sample_items = [
        {
            "title": "Inception",
            "description": "A thief who steals corporate secrets through the use of dream-sharing technology.",
            "category": "movie",
            "metadata": {"year": 2010, "genre": ["Sci-Fi", "Action"]}
        },
        {
            "title": "Dune: Part Two",
            "description": "Paul Atreides unites with Chani and the Fremen while seeking revenge.",
            "category": "movie",
            "metadata": {"year": 2024, "genre": ["Sci-Fi", "Adventure"]}
        },
        {
            "title": "The Psychology of Money",
            "description": "Timeless lessons on wealth, greed, and happiness.",
            "category": "book",
            "metadata": {"year": 2020}
        },
        {
            "title": "Atomic Habits",
            "description": "An easy & proven way to build good habits & break bad ones.",
            "category": "book",
            "metadata": {"year": 2018}
        }
    ]

    for item in sample_items:
        text_for_embedding = f"{item['title']}: {item['description']}"
        embedding = get_embedding(text_for_embedding)
        
        cur.execute("""
            INSERT INTO items (title, description, category, metadata, embedding)
            VALUES (%s, %s, %s, %s, %s)
        """, (item['title'], item['description'], item['category'], 
              json.dumps(item.get('metadata')), embedding))
    
    conn.commit()
    cur.close()
    conn.close()
    print(f"✅ Successfully seeded {len(sample_items)} items!")

if __name__ == "__main__":
    seed_database()