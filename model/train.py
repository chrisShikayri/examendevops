# model/train.py
import joblib
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Datos de entrenamiento muy simples — reproducibles
X = [
    "me encanta este examen",
    "odio los errores",
    "este es un gran día",
    "estoy triste",
    "muy feliz",
    "no me gusta esto"
]
y = [1, 0, 1, 0, 1, 0]  # 1 = positivo, 0 = negativo (ejemplo)

pipeline = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("clf", LogisticRegression(max_iter=500))
])

pipeline.fit(X, y)

# Guarda el modelo
joblib.dump(pipeline, "model/model.pkl")
print("Modelo guardado en model/model.pkl")
