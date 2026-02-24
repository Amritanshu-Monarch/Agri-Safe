"""
Spray Advisory Service
───────────────────────
This is the CORE INNOVATION of Agri-Safe.
Combines disease detection results with real-time weather to prevent:
  - Pesticide washout (spraying before rain)
  - Financial loss for farmers
  - Chemical runoff and environmental pollution
"""
from app.services.cnn_service import get_treatment
from app.config import settings


# Advisory decision constants
SAFE_TO_SPRAY    = "SAFE_TO_SPRAY"
HOLD_SPRAY       = "HOLD_SPRAY"
NO_ACTION_NEEDED = "NO_ACTION_NEEDED"


def generate_spray_advisory(detection: dict, weather: dict) -> dict:
    """
    Decision Logic:
    ┌─────────────────┬──────────────────┬─────────────────────────┐
    │ Disease Found?  │ Rain Expected?   │ Decision                │
    ├─────────────────┼──────────────────┼─────────────────────────┤
    │ No (Healthy)    │ Any              │ NO_ACTION_NEEDED        │
    │ Yes             │ No               │ SAFE_TO_SPRAY           │
    │ Yes             │ Yes (>40%)       │ HOLD_SPRAY ⚠️           │
    │ Low confidence  │ Any              │ HOLD_SPRAY (uncertain)  │
    └─────────────────┴──────────────────┴─────────────────────────┘
    """
    disease_name  = detection["disease_name"]
    confidence    = detection["confidence"]
    is_healthy    = detection["is_healthy"]
    rain_expected = weather["rain_expected_12h"]
    rain_prob     = weather["rain_probability_percent"]
    treatment     = get_treatment(disease_name)

    # ── Case 1: Plant is healthy ─────────────────────────────────────────────
    if is_healthy:
        return {
            "decision": NO_ACTION_NEEDED,
            "reason": (
                f"Your crop appears healthy (confidence: {confidence*100:.0f}%). "
                "No pesticide or fungicide application is required at this time. "
                "Continue regular monitoring."
            ),
            "treatment": "No treatment needed. Maintain good agricultural practices.",
        }

    # ── Case 2: Low confidence detection ────────────────────────────────────
    if confidence < settings.CONFIDENCE_THRESHOLD:
        return {
            "decision": HOLD_SPRAY,
            "reason": (
                f"Disease detected ({disease_name}) but with low confidence "
                f"({confidence*100:.0f}%). Please retake the photo in good lighting "
                "or consult an agricultural officer before applying any treatment."
            ),
            "treatment": treatment,
        }

    # ── Case 3: Disease confirmed + Rain expected ────────────────────────────
    if rain_expected:
        return {
            "decision": HOLD_SPRAY,
            "reason": (
                f"⚠️ Disease detected: {_format_name(disease_name)} "
                f"(confidence: {confidence*100:.0f}%). "
                f"However, rain is forecast in the next 12 hours "
                f"(probability: {rain_prob:.0f}%). "
                "Spraying now would cause the pesticide to wash off, "
                "wasting your money and polluting the soil. "
                "Wait for the rain to pass, then apply treatment."
            ),
            "treatment": treatment,
        }

    # ── Case 4: Disease confirmed + Clear weather ────────────────────────────
    return {
        "decision": SAFE_TO_SPRAY,
        "reason": (
            f"✅ Disease detected: {_format_name(disease_name)} "
            f"(confidence: {confidence*100:.0f}%). "
            f"Weather is favorable — only {rain_prob:.0f}% chance of rain. "
            "This is a good window to apply treatment. "
            "Apply early morning or evening for best absorption."
        ),
        "treatment": treatment,
    }


def _format_name(disease_name: str) -> str:
    """Convert 'Potato___Late_blight' → 'Potato - Late Blight'"""
    parts = disease_name.split("___")
    if len(parts) == 2:
        crop, disease = parts
        return f"{crop} - {disease.replace('_', ' ').title()}"
    return disease_name.replace("_", " ").title()
