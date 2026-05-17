from fastapi import APIRouter, Depends, HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os

from app.models.schemas import FeedbackCreate

load_dotenv()

router = APIRouter()

@router.post("/feedback")
async def save_feedback(feedback: FeedbackCreate):
    conn = None
    try:
        conn = psycopg2.connect(os.getenv("DATABASE_URL"))
        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute("""
            INSERT INTO user_feedback (user_id, item_id, rating, feedback_text)
            VALUES (%s, %s, %s, %s)
            RETURNING id, created_at
        """, (feedback.user_id, feedback.item_id, feedback.rating, feedback.feedback_text))

        result = cur.fetchone()
        conn.commit()

        return {
            "message": "Feedback saved successfully",
            "feedback_id": result["id"],
            "created_at": result["created_at"]
        }

    except Exception as e:
        print("🔥 ERROR in feedback:", str(e))
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            cur.close()
            conn.close()


@router.get("/feedback/history")
async def get_feedback_history(user_id: str = "default_user"):
    conn = None
    try:
        conn = psycopg2.connect(os.getenv("DATABASE_URL"))
        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute("""
            SELECT f.id, f.item_id, i.title, f.rating, f.feedback_text, f.created_at
            FROM user_feedback f
            JOIN items i ON f.item_id = i.id
            WHERE f.user_id = %s
            ORDER BY f.created_at DESC
        """, (user_id,))

        history = cur.fetchall()
        return {"user_id": user_id, "feedback_history": [dict(row) for row in history]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            cur.close()
            conn.close()