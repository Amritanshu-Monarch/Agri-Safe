from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.services.cnn_service import predict_disease
from app.services.weather_service import get_weather_advisory
from app.services.advisory_service import generate_spray_advisory
from pydantic import BaseModel
from typing import Optional
import shutil, os, uuid

router = APIRouter()

class DetectionResponse(BaseModel):
    disease_name: str
    confidence: float
    is_healthy: bool
    weather_summary: dict
    spray_advisory: str          # "SAFE_TO_SPRAY" | "HOLD_SPRAY" | "NO_ACTION_NEEDED"
    advisory_reason: str
    treatment_suggestion: str


@router.post("/scan", response_model=DetectionResponse)
async def scan_crop(
    image: UploadFile = File(..., description="Crop leaf image"),
    latitude: float  = Form(..., description="Farmer's latitude for weather lookup"),
    longitude: float = Form(..., description="Farmer's longitude for weather lookup"),
):
    """
    Core endpoint: 
    1. Run CNN model on uploaded image → get disease name + confidence
    2. Fetch weather forecast for farmer's location
    3. Combine both to generate a context-aware spray advisory
    """
    # ── Step 1: Save image temporarily ──────────────────────────────────────
    temp_path = f"/tmp/{uuid.uuid4().hex}_{image.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    try:
        # ── Step 2: Run disease detection ───────────────────────────────────
        detection = predict_disease(temp_path)

        # ── Step 3: Get weather context ─────────────────────────────────────
        weather = await get_weather_advisory(latitude, longitude)

        # ── Step 4: Generate combined advisory ──────────────────────────────
        advisory = generate_spray_advisory(detection, weather)

        return DetectionResponse(
            disease_name        = detection["disease_name"],
            confidence          = detection["confidence"],
            is_healthy          = detection["is_healthy"],
            weather_summary     = weather,
            spray_advisory      = advisory["decision"],
            advisory_reason     = advisory["reason"],
            treatment_suggestion= advisory["treatment"],
        )

    finally:
        os.remove(temp_path)  # Clean up temp file
