import joblib
import numpy as np
from datetime import datetime

# -------------------------------
# 1. Load Saved Components
# -------------------------------
model = joblib.load("models/model.pkl")
scaler = joblib.load("models/scaler.pkl")
label_encoder = joblib.load("models/label_encoder.pkl")

# -------------------------------
# 2. Normal Ranges (for display)
# -------------------------------
NORMAL_RANGES = {
    "Age": "18–35 years",
    "SystolicBP": "90–120 mmHg",
    "DiastolicBP": "60–80 mmHg",
    "BS": "4–7 mmol/L",
    "BodyTemp": "36.5–37.5 °C",
    "HeartRate": "60–100 bpm"
}

# -------------------------------
# 3. Prediction Function
# -------------------------------
def predict_risk(age, systolic_bp, diastolic_bp, bs, body_temp, heart_rate):
    
    # Create input array
    import pandas as pd

    input_data = pd.DataFrame([{
    "Age": age,
    "SystolicBP": systolic_bp,
    "DiastolicBP": diastolic_bp,
    "BS": bs,
    "BodyTemp": body_temp,
    "HeartRate": heart_rate
    }])

    input_scaled = scaler.transform(input_data)
    
    # Prediction
    prediction = model.predict(input_scaled)[0]
    
    # Probability (confidence)
    probabilities = model.predict_proba(input_scaled)[0]
    confidence = float(np.max(probabilities))
    
    # Convert label
    risk_label = label_encoder.inverse_transform([prediction])[0]
    
    # Timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Output dictionary
    result = {
        "risk_level": risk_label,
        "confidence": round(confidence * 100, 2),
        "timestamp": timestamp,
        "input_values": {
            "Age": age,
            "SystolicBP": systolic_bp,
            "DiastolicBP": diastolic_bp,
            "BloodSugar": bs,
            "BodyTemp": body_temp,
            "HeartRate": heart_rate
        },
        "normal_ranges": NORMAL_RANGES
    }
    
    return result


# -------------------------------
# 4. Test Run (Optional)
# -------------------------------
if __name__ == "__main__":
    
    test = predict_risk(
        age=30,
        systolic_bp=130,
        diastolic_bp=85,
        bs=8.0,
        body_temp=37.5,
        heart_rate=90
    )
    
    print("\nPrediction Result:\n")
    print(test)

