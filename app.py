# app.py
from flask import Flask, request, jsonify, render_template_string
import joblib
import os

MODEL_PATH = os.environ.get("MODEL_PATH", "model/model.pkl")

app = Flask(__name__)
model = joblib.load(MODEL_PATH)

# ----------- Página bonita -----------
HTML_PAGE = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Exam DevOps - Chris Shikayri</title>

<style>
    body {
        font-family: 'Arial', sans-serif;
        background: linear-gradient(135deg, #5C4EE5, #8E63F6);
        color: white;
        text-align: center;
        padding: 40px;
    }

    h1 {
        font-size: 42px;
        margin-bottom: 10px;
        text-shadow: 2px 2px 6px rgba(0,0,0,0.3);
    }

    .card {
        background: rgba(255,255,255,0.15);
        padding: 30px;
        border-radius: 18px;
        width: 450px;
        margin: auto;
        box-shadow: 0 8px 20px rgba(0,0,0,0.2);
        backdrop-filter: blur(10px);
    }

    input[type="text"] {
        width: 90%;
        padding: 12px;
        border-radius: 10px;
        border: none;
        margin-top: 10px;
        margin-bottom: 20px;
        font-size: 16px;
    }

    button {
        padding: 12px 25px;
        font-size: 16px;
        border: none;
        border-radius: 12px;
        background: #FFD93D;
        color: #333;
        font-weight: bold;
        cursor: pointer;
        transition: 0.3s;
    }

    button:hover {
        background: #ffca1c;
    }

    #result {
        margin-top: 25px;
        font-size: 18px;
    }
</style>

</head>
<body>

<h1>🔮 Modelo de Predicción</h1>
<p>Propietario: <strong>Chris Shikayri Bautista</strong></p>

<div class="card">
    <h2>Ingresa un texto para predecir</h2>

    <input type="text" id="texto" placeholder="Escribe algo aquí...">

    <button onclick="enviar()">Predecir</button>

    <div id="result"></div>
</div>

<script>
function enviar() {
    let txt = document.getElementById("texto").value;

    fetch("/predict", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({text: txt})
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("result").innerHTML = `
            <br><strong>Texto:</strong> ${data.text || '-'}
            <br><strong>Predicción:</strong> ${data.prediction}
            <br><strong>Probabilidad:</strong> ${data.probability}
        `;
    });
}
</script>

</body>
</html>
"""

# ------- Ruta bonita ---------
@app.route("/")
def home():
    return render_template_string(HTML_PAGE)

# ------- Ruta JSON original ------
@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json() or {}
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "text field required"}), 400

    try:
        pred = model.predict([text])[0]
        proba = max(model.predict_proba([text])[0]).item()
    except Exception as e:
        return jsonify({"error": "model failure", "details": str(e)}), 500

    return jsonify({"text": text, "prediction": int(pred), "probability": proba})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
