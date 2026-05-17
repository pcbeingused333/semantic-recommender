from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from dotenv import load_dotenv

load_dotenv()

# ←←← CREAMOS LA APP ANTES DE CUALQUIER IMPORT DE ROUTERS ←←←
app = FastAPI(
    title="Semantic Recommender",
    description="Intelligent recommendations using embeddings + pgvector",
    version="1.0.0"
)

# CORS (para que el frontend pueda conectar)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Importamos los routers DESPUÉS de crear 'app'
from app.routers.recommendations import router as recommendations_router
from app.routers.feedback import router as feedback_router

# Registramos los routers
app.include_router(recommendations_router, prefix="/api", tags=["recommendations"])
app.include_router(feedback_router, prefix="/api", tags=["feedback"])

@app.get("/")
async def root():
    return {
        "message": "Semantic Recommender API is running 🚀",
        "docs": "/docs"
    }

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)