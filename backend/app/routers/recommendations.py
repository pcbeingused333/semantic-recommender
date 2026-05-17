from fastapi import APIRouter, HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
import numpy as np

from app.embeddings import get_embedding
from app.models.schemas import RecommendationRequest

load_dotenv()

router = APIRouter()

def get_user_profile(user_id: str = "default_user"):
    """Calcula embedding promedio de los ítems que le gustaron al usuario"""
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    cur = conn.cursor()

    cur.execute("""
        SELECT i.embedding
        FROM user_feedback f
        JOIN items i ON f.item_id = i.id
        WHERE f.user_id = %s AND f.rating >= 4
    """, (user_id,))

    liked_embeddings = cur.fetchall()
    cur.close()
    conn.close()

    if not liked_embeddings:
        return None

    # Promedio de embeddings liked
    emb_array = np.array([emb[0] for emb in liked_embeddings])
    return emb_array.mean(axis=0).tolist()


@router.post("/recommend")
async def get_recommendations(request: RecommendationRequest, user_id: str = "default_user"):
    try:
        query_embedding = get_embedding(request.query)
        user_profile = get_user_profile(user_id)

        conn = psycopg2.connect(os.getenv("DATABASE_URL"))
        cur = conn.cursor(cursor_factory=RealDictCursor)

        # Si tenemos perfil de usuario → combinamos embeddings
        if user_profile:
            # Combinación: 70% query + 30% perfil del usuario
            combined = np.array(query_embedding) * 0.7 + np.array(user_profile) * 0.3
            combined = combined.tolist()
            emb_param = combined
        else:
            emb_param = query_embedding

        cur.execute("""
            SELECT 
                id,
                title,
                description,
                category,
                metadata,
                1 - (embedding <=> %s::vector) as similarity
            FROM items
            WHERE (%s IS NULL OR category = %s)
            ORDER BY embedding <=> %s::vector
            LIMIT %s
        """, (emb_param, request.category, request.category, emb_param, request.top_k))

        rows = cur.fetchall()
        cur.close()
        conn.close()

        recommendations = [dict(row) for row in rows]

        return {
            "query": request.query,
            "user_id": user_id,
            "personalized": user_profile is not None,
            "recommendations": recommendations
        }

    except Exception as e:
        print("🔥 ERROR in /recommend:", str(e))
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))