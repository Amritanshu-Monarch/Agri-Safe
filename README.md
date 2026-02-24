# Agri-Safe



# Agri-Safe Backend

Context-Aware Crop Disease Detection & Advisory API

## Architecture

```
Frontend (HTML/JS)
       │
       ▼
FastAPI Backend (Python)
       ├── POST /api/detect/scan    ← Image upload → CNN → Weather → Advisory
       ├── POST /api/chat/ask       ← RAG Chatbot (Gemini + Agriculture Manual)
       └── GET  /api/weather/current ← Weather widget
       │
       ├── CNN Service (MobileNetV2 / TFLite)
       ├── Weather Service (OpenWeatherMap)
       ├── Advisory Engine (Spray decision logic)
       └── RAG Chatbot (Gemini + PDF knowledge base)
```

## Setup

### 1. Install dependencies
```bash
cd agrisafe-backend
pip install -r requirements.txt
```

### 2. Configure API keys
```bash
cp .env.example .env
# Edit .env with your actual keys:
#   OPENWEATHER_API_KEY = from openweathermap.org (free tier works)
#   GEMINI_API_KEY      = from aistudio.google.com (free)
```

### 3. Add your CNN model
Place your trained model file at: `app/models/crop_disease_model.h5`
- Accepts `.h5` (Keras) or `.tflite` (TFLite Lite)
- Must output class probabilities for PlantVillage classes
- Update `DISEASE_CLASSES` list in `app/services/cnn_service.py` if your classes differ

### 4. Add knowledge base (optional but recommended)
Place your agriculture PDF at: `app/data/agriculture_manual.pdf`
- If not provided, a built-in set of crop guidelines is used as fallback

### 5. Run the server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 6. Test the API
Visit: http://localhost:8000/docs (Swagger UI — auto-generated)

## API Endpoints

### POST /api/detect/scan
Upload a crop image to get disease detection + spray advisory.

**Form Data:**
- `image` (file) — crop leaf photo
- `latitude` (float) — GPS latitude
- `longitude` (float) — GPS longitude

**Response:**
```json
{
  "disease_name": "Potato___Late_blight",
  "confidence": 0.94,
  "is_healthy": false,
  "weather_summary": { "rain_probability_percent": 65, "rain_expected_12h": true, ... },
  "spray_advisory": "HOLD_SPRAY",
  "advisory_reason": "⚠️ Rain expected in 12 hours. Wait before spraying.",
  "treatment_suggestion": "Apply Mancozeb 75% WP @ 2g/litre after rain passes."
}
```

### POST /api/chat/ask
Ask the RAG chatbot a farming question.

**Body:**
```json
{ "message": "potato mein kaun si dawai use karein?", "language": "hi" }
```

### GET /api/weather/current?lat=28.6&lon=77.2
Get weather forecast for a location.

## Frontend Integration
See `frontend-integration.js` for ready-to-use JavaScript functions to connect your HTML frontend.

## Spray Decision Logic

| Disease Found | Rain Expected | Decision        |
|---------------|---------------|-----------------|
| No (Healthy)  | Any           | NO_ACTION_NEEDED|
| Yes           | No (<40%)     | SAFE_TO_SPRAY ✅|
| Yes           | Yes (>40%)    | HOLD_SPRAY ⚠️   |
| Low confidence| Any           | HOLD_SPRAY ⚠️   |
