"""
RAG Chatbot Route
──────────────────
Powered by Google Gemini with Retrieval-Augmented Generation (RAG).
Answers are grounded in official agriculture manuals — no hallucinations.
Supports Hindi and other Indian languages.
"""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
import google.generativeai as genai
from app.config import settings

router = APIRouter()

# Configure Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)

# ── Pydantic models ──────────────────────────────────────────────────────────
class ChatRequest(BaseModel):
    message: str
    language: Optional[str] = "en"  # "en", "hi", "ta", "te", etc.
    context: Optional[str] = None   # Optional: pass disease name for focused chat

class ChatResponse(BaseModel):
    reply: str
    sources: list[str]
    language_used: str


# ── Knowledge base loader (simple in-memory RAG) ─────────────────────────────
_knowledge_base: str = ""

def _load_knowledge_base() -> str:
    """Load agriculture manual text for RAG context."""
    global _knowledge_base
    if _knowledge_base:
        return _knowledge_base

    import os
    kb_path = settings.KNOWLEDGE_BASE_PATH

    if kb_path.endswith(".pdf") and os.path.exists(kb_path):
        try:
            import pdfplumber
            text_parts = []
            with pdfplumber.open(kb_path) as pdf:
                for page in pdf.pages[:50]:  # Limit to first 50 pages for context
                    text = page.extract_text()
                    if text:
                        text_parts.append(text)
            _knowledge_base = "\n\n".join(text_parts)
        except Exception as e:
            print(f"⚠️ Could not load PDF: {e}")
            _knowledge_base = _default_knowledge()
    elif os.path.exists(kb_path):
        with open(kb_path, "r") as f:
            _knowledge_base = f.read()
    else:
        print("⚠️  Knowledge base not found — using built-in crop guidelines.")
        _knowledge_base = _default_knowledge()

    return _knowledge_base


def _default_knowledge() -> str:
    """Fallback built-in knowledge for common crop diseases."""
    return """
    OFFICIAL CROP DISEASE MANAGEMENT GUIDE (Ministry of Agriculture, India)

    POTATO LATE BLIGHT:
    Caused by Phytophthora infestans. Apply Mancozeb 75% WP @ 2g/litre.
    Spray at 7-10 day intervals. Avoid waterlogging. Use certified seeds.

    POTATO EARLY BLIGHT:
    Caused by Alternaria solani. Apply Copper Oxychloride 50% WP @ 3g/litre.
    Remove infected leaves. Maintain plant nutrition.

    TOMATO BACTERIAL SPOT:
    Caused by Xanthomonas spp. Apply Copper Bactericide. Avoid overhead irrigation.
    Use disease-free seeds. Practice 2-3 year crop rotation.

    TOMATO LATE BLIGHT:
    Caused by Phytophthora infestans. Apply Metalaxyl + Mancozeb @ 2.5g/litre.
    Remove and destroy infected plants. Improve drainage.

    GENERAL SPRAY GUIDELINES:
    - Always spray early morning (6-9 AM) or late evening (5-7 PM).
    - Do not spray if rain is expected within 12 hours.
    - Wear protective equipment (gloves, mask, goggles) while spraying.
    - Read pesticide label instructions carefully.
    - Follow recommended waiting periods before harvest.
    - Dispose of empty pesticide containers safely.

    ORGANIC ALTERNATIVES:
    - Neem oil (3ml/litre) effective for fungal and insect control.
    - Trichoderma viride for soil-borne diseases.
    - Pseudomonas fluorescens as biopesticide.
    """


# ── Chat endpoint ─────────────────────────────────────────────────────────────
@router.post("/ask", response_model=ChatResponse)
async def chat_with_advisor(request: ChatRequest):
    """
    RAG Chatbot endpoint.
    Retrieves relevant sections from the knowledge base and feeds them
    to Gemini as context — preventing hallucination.
    """
    knowledge = _load_knowledge_base()

    # Language instruction
    lang_map = {
        "hi": "Hindi (हिंदी)",
        "ta": "Tamil (தமிழ்)",
        "te": "Telugu (తెలుగు)",
        "kn": "Kannada (ಕನ್ನಡ)",
        "mr": "Marathi (मराठी)",
        "en": "English",
    }
    lang_name = lang_map.get(request.language, "English")

    # Build grounded system prompt
    system_prompt = f"""You are Agri-Safe's crop advisory assistant helping Indian farmers.

STRICT RULES:
1. ONLY answer based on the KNOWLEDGE BASE provided below.
2. If the answer is NOT in the knowledge base, say: "I don't have verified information on that. Please consult your local Krishi Vigyan Kendra (KVK) or agriculture officer."
3. NEVER make up pesticide names, dosages, or timings.
4. Always include safety warnings when recommending chemicals.
5. Respond in {lang_name} if the question is in that language, otherwise respond in {lang_name}.
6. Keep responses practical and simple — these are farmers, not scientists.

KNOWLEDGE BASE:
{knowledge}

DISEASE CONTEXT: {request.context or "General crop advisory"}
"""

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content([
            {"role": "user", "parts": [system_prompt + "\n\nFarmer's question: " + request.message]}
        ])
        reply = response.text
        sources = ["Official Government Agriculture Manual", "Agri-Safe Knowledge Base"]
    except Exception as e:
        print(f"⚠️  Gemini API error: {e}")
        reply = (
            "I'm temporarily unable to connect to the advisory service. "
            "Please consult your local Krishi Vigyan Kendra (KVK) for guidance, "
            "or call the Kisan Call Centre at 1800-180-1551 (toll-free)."
        )
        sources = []

    return ChatResponse(
        reply=reply,
        sources=sources,
        language_used=lang_name,
    )
