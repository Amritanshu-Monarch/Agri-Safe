from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import detect, chat, weather

app = FastAPI(
    title="Agri-Safe API",
    description="Context-Aware Crop Disease Detection & Advisory Backend",
    version="1.0.0"
)

# Allow frontend (HTML/JS) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(detect.router, prefix="/api/detect", tags=["Disease Detection"])
app.include_router(chat.router,   prefix="/api/chat",   tags=["RAG Chatbot"])
app.include_router(weather.router, prefix="/api/weather", tags=["Weather"])

@app.get("/")
def root():
    return {"message": "Agri-Safe Backend is running ✅"}
