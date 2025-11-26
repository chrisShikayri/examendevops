# app.py
from flask import Flask, request, jsonify
import joblib
import os

MODEL_PATH = os.environ.get("MODEL_PATH", "model/model.pkl")

app = Flask(__name__)

# Cargar modelo simple (sklearn)
model = joblib.load(MODEL_PATH)

@app.route("/")
def index():
    return jsonify({"app": "examendevops", "owner": "chrisShikayri", "apellido": "Bautista"})

@app.route("/predict", methods=["POST"])
def predict():
    """
    Recibe JSON {"text": "..."} y devuelve una 'predicción' (0/1) y probabilidad.
    """
    data = request.get_json() or {}
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "text field required"}), 400

    # Aquí usamos una representación muy simple: contar longitud, etc.
    # Nuestro 'modelo' entrenado hará la predicción.
    try:
        pred = model.predict([text])[0]
        proba = max(model.predict_proba([text])[0]).item()
    except Exception as e:
        return jsonify({"error": "model failure", "details": str(e)}), 500

    return jsonify({"text": text, "prediction": int(pred), "probability": proba})
