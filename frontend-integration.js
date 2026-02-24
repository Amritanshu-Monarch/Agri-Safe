/**
 * ═══════════════════════════════════════════════════════════
 *  AGRI-SAFE FRONTEND ↔ BACKEND INTEGRATION
 *  Add this <script> to the bottom of your index.html
 * ═══════════════════════════════════════════════════════════
 */

const API_BASE = "http://localhost:8000/api";   // Change to your deployed URL

// ─────────────────────────────────────────────────────────────────
// 1. SCAN CROP — Upload image + location → get disease + advisory
// ─────────────────────────────────────────────────────────────────
async function scanCrop(imageFile, latitude, longitude) {
    const formData = new FormData();
    formData.append("image", imageFile);
    formData.append("latitude", latitude);
    formData.append("longitude", longitude);

    const response = await fetch(`${API_BASE}/detect/scan`, {
        method: "POST",
        body: formData,
        // ✅ Don't set Content-Type header — browser sets it with boundary
    });

    if (!response.ok) throw new Error("Detection failed: " + response.statusText);

    const result = await response.json();

    /**
     * result = {
     *   disease_name:        "Potato___Late_blight",
     *   confidence:           0.94,
     *   is_healthy:           false,
     *   weather_summary: {
     *     current_condition:        "Partly Cloudy",
     *     temperature_c:             26.5,
     *     humidity_percent:          72.0,
     *     rain_probability_percent:  65.0,
     *     rain_expected_12h:         true,
     *   },
     *   spray_advisory:      "HOLD_SPRAY",
     *   advisory_reason:     "⚠️ Disease detected: Potato - Late Blight ... rain expected ...",
     *   treatment_suggestion:"Apply Mancozeb fungicide ...",
     * }
     */
    return result;
}

// Example: Hook up to your "Scan Your Crop" button
document.getElementById("scanBtn")?.addEventListener("click", async () => {
    const fileInput = document.getElementById("cropImageInput");
    if (!fileInput?.files[0]) return alert("Please select an image first.");

    // Get user's GPS location
    navigator.geolocation.getCurrentPosition(async (pos) => {
        try {
            showLoader(true);
            const result = await scanCrop(
                fileInput.files[0],
                pos.coords.latitude,
                pos.coords.longitude
            );
            renderAdvisoryCard(result);
        } catch (err) {
            console.error(err);
            alert("Something went wrong. Please try again.");
        } finally {
            showLoader(false);
        }
    }, () => {
        // Fallback: use a default location if GPS denied
        alert("Please allow location access for weather-based advice.");
    });
});

// ─────────────────────────────────────────────────────────────────
// 2. CHATBOT — Send a message to the RAG advisory bot
// ─────────────────────────────────────────────────────────────────
async function askChatbot(message, language = "en", diseaseContext = null) {
    const response = await fetch(`${API_BASE}/chat/ask`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            message: message,
            language: language,
            context: diseaseContext,
        }),
    });

    if (!response.ok) throw new Error("Chat failed: " + response.statusText);
    const data = await response.json();

    /**
     * data = {
     *   reply:         "Apply Mancozeb @ 2g/litre...",
     *   sources:       ["Official Government Agriculture Manual"],
     *   language_used: "English"
     * }
     */
    return data;
}

// ─────────────────────────────────────────────────────────────────
// 3. WEATHER — Fetch weather for a location
// ─────────────────────────────────────────────────────────────────
async function getWeather(latitude, longitude) {
    const response = await fetch(
        `${API_BASE}/weather/current?lat=${latitude}&lon=${longitude}`
    );
    if (!response.ok) throw new Error("Weather fetch failed");
    return await response.json();
}

// ─────────────────────────────────────────────────────────────────
// UI HELPERS
// ─────────────────────────────────────────────────────────────────
function renderAdvisoryCard(result) {
    const colors = {
        SAFE_TO_SPRAY:    "bg-green-100 border-green-400 text-green-800",
        HOLD_SPRAY:       "bg-red-100 border-red-400 text-red-800",
        NO_ACTION_NEEDED: "bg-blue-100 border-blue-400 text-blue-800",
    };

    const icons = {
        SAFE_TO_SPRAY:    "✅",
        HOLD_SPRAY:       "⚠️",
        NO_ACTION_NEEDED: "🌱",
    };

    const card = document.getElementById("advisoryCard");
    if (!card) return;

    const colorClass = colors[result.spray_advisory] || colors.HOLD_SPRAY;
    const icon       = icons[result.spray_advisory]  || "ℹ️";

    card.innerHTML = `
        <div class="border-2 rounded-xl p-6 ${colorClass}">
            <h3 class="text-2xl font-bold mb-2">${icon} ${result.spray_advisory.replace(/_/g, " ")}</h3>
            <p class="text-sm mb-4">${result.advisory_reason}</p>
            <hr class="border-current opacity-30 mb-4"/>
            <p class="font-semibold">🌿 Disease: ${result.disease_name.replace(/___/g, " - ").replace(/_/g, " ")}</p>
            <p class="text-sm">Confidence: ${(result.confidence * 100).toFixed(0)}%</p>
            <p class="font-semibold mt-3">💊 Treatment:</p>
            <p class="text-sm">${result.treatment_suggestion}</p>
            <p class="font-semibold mt-3">🌤 Weather:</p>
            <p class="text-sm">
                ${result.weather_summary.current_condition} | 
                ${result.weather_summary.temperature_c}°C | 
                Rain chance: ${result.weather_summary.rain_probability_percent}%
            </p>
        </div>
    `;
    card.scrollIntoView({ behavior: "smooth" });
}

function showLoader(show) {
    const loader = document.getElementById("loader");
    if (loader) loader.classList.toggle("hidden", !show);
}
