"""
CNN Disease Detection Service
─────────────────────────────
Uses a MobileNetV2-based model (as described in the Agri-Safe frontend).
Supports both .h5 (TensorFlow/Keras) and .tflite (TensorFlow Lite) models.

Supported disease classes (PlantVillage dataset — extend as needed):
"""
import numpy as np
from PIL import Image
from app.config import settings

# ── Disease class labels ────────────────────────────────────────────────────
# These map model output indices → human-readable disease names.
# Update this list to match YOUR model's training classes IN ORDER.
DISEASE_CLASSES = [
    "Apple___Apple_scab",
    "Apple___Black_rot",
    "Apple___Cedar_apple_rust",
    "Apple___healthy",
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
    "Corn_(maize)___Common_rust_",
    "Corn_(maize)___Northern_Leaf_Blight",
    "Corn_(maize)___healthy",
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy",
    "Tomato___Bacterial_spot",
    "Tomato___Early_blight",
    "Tomato___Late_blight",
    "Tomato___Leaf_Mold",
    "Tomato___Septoria_leaf_spot",
    "Tomato___healthy",
]

# Treatment advice keyed by disease name
TREATMENT_MAP = {
    "Potato___Late_blight":
        "Apply Mancozeb or Chlorothalonil-based fungicide. Remove and destroy infected plants.",
    "Potato___Early_blight":
        "Apply copper-based fungicide. Ensure proper crop rotation next season.",
    "Tomato___Bacterial_spot":
        "Apply copper bactericide. Avoid overhead irrigation.",
    "Tomato___Early_blight":
        "Apply Azoxystrobin fungicide. Remove lower infected leaves.",
    "Tomato___Late_blight":
        "Apply Metalaxyl fungicide immediately. Destroy infected plants.",
    "Corn_(maize)___Common_rust_":
        "Apply Propiconazole fungicide. Plant resistant varieties next season.",
    "Apple___Apple_scab":
        "Apply Captan or Myclobutanil fungicide. Rake and remove fallen leaves.",
    # Healthy — no treatment needed
    "default": "Consult your local agriculture extension officer for specific guidance.",
}

# ── Model loading (singleton — load once at startup) ────────────────────────
_model = None

def _load_model():
    global _model
    if _model is not None:
        return _model

    model_path = settings.MODEL_PATH

    if model_path.endswith(".tflite"):
        import tflite_runtime.interpreter as tflite
        _model = {"type": "tflite", "interpreter": tflite.Interpreter(model_path=model_path)}
        _model["interpreter"].allocate_tensors()
    else:
        import tensorflow as tf
        _model = {"type": "keras", "model": tf.keras.models.load_model(model_path)}

    return _model


def _preprocess_image(image_path: str) -> np.ndarray:
    """Resize and normalize image to 224×224 as expected by MobileNetV2."""
    img = Image.open(image_path).convert("RGB")
    img = img.resize((224, 224))
    arr = np.array(img, dtype=np.float32) / 255.0  # Normalize to [0, 1]
    return np.expand_dims(arr, axis=0)              # Add batch dimension


def predict_disease(image_path: str) -> dict:
    """
    Run CNN inference on the given image path.
    Returns: { disease_name, confidence, is_healthy, raw_class }
    
    NOTE: If MODEL_PATH doesn't exist yet (during development), 
    returns a mock result so you can test the rest of the pipeline.
    """
    import os
    if not os.path.exists(settings.MODEL_PATH):
        # ── MOCK RESPONSE for development/testing ───────────────────────────
        print("⚠️  Model not found — returning mock detection result.")
        return {
            "disease_name": "Potato___Late_blight",
            "confidence": 0.94,
            "is_healthy": False,
            "raw_class": "Potato___Late_blight",
        }

    model_bundle = _load_model()
    img = _preprocess_image(image_path)

    if model_bundle["type"] == "tflite":
        interpreter = model_bundle["interpreter"]
        input_details  = interpreter.get_input_details()
        output_details = interpreter.get_output_details()
        interpreter.set_tensor(input_details[0]["index"], img)
        interpreter.invoke()
        predictions = interpreter.get_tensor(output_details[0]["index"])[0]
    else:
        predictions = model_bundle["model"].predict(img)[0]

    class_idx    = int(np.argmax(predictions))
    confidence   = float(predictions[class_idx])
    disease_name = DISEASE_CLASSES[class_idx] if class_idx < len(DISEASE_CLASSES) else "Unknown"
    is_healthy   = "healthy" in disease_name.lower()

    return {
        "disease_name": disease_name,
        "confidence": round(confidence, 4),
        "is_healthy": is_healthy,
        "raw_class": disease_name,
    }


def get_treatment(disease_name: str) -> str:
    return TREATMENT_MAP.get(disease_name, TREATMENT_MAP["default"])
