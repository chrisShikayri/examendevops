# tests/test_app.py
import json
from app import app

def test_index():
    client = app.test_client()
    rv = client.get("/")
    assert rv.status_code == 200
    data = rv.get_json()
    assert data["apellido"].lower() == "bautista"

def test_predict_ok():
    client = app.test_client()
    rv = client.post("/predict", json={"text": "me encanta esto"})
    assert rv.status_code == 200
    data = rv.get_json()
    assert "prediction" in data
    assert 0 <= data["probability"] <= 1

def test_predict_bad_request():
    client = app.test_client()
    rv = client.post("/predict", json={})
    assert rv.status_code == 400
