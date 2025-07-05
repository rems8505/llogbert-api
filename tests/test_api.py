import sys
import os  # Also needed for path handling

# Add the root directory to sys.path so app.py can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app  # Now this will work if app.py is at the root
from fastapi.testclient import TestClient

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "LLogBERT API is running!"}

def test_predict_valid_log():
    sample_log = {
        "text": "2023-07-01 12:34:56,123 INFO nova.compute.manager: Instance started successfully"
    }
    response = client.post("/predict", json=sample_log)
    assert response.status_code == 200
    result = response.json()
    assert "label" in result
    assert "logits" in result
    assert isinstance(result["label"], int)
    assert isinstance(result["logits"], list)

def test_predict_invalid_input():
    response = client.post("/predict", json={"log": "missing expected 'text' key"})
    assert response.status_code == 422
