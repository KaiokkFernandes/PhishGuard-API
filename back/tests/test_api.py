import pytest
from fastapi.testclient import TestClient
from main import app

# Criar cliente de teste
client = TestClient(app)

def test_root_endpoint():
    """Testa o endpoint raiz"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data

def test_health_endpoint():
    """Testa o endpoint de health check"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_predict_endpoint_valid_url():
    """Testa predição com URL válida"""
    test_url = {"url": "https://www.google.com"}
    response = client.post("/api/v1/predict", json=test_url)
    assert response.status_code == 200
    data = response.json()
    assert "url" in data
    assert "is_phishing" in data
    assert "confidence" in data
    assert "risk_level" in data
    assert isinstance(data["is_phishing"], bool)
    assert 0 <= data["confidence"] <= 1

def test_predict_endpoint_suspicious_url():
    """Testa predição com URL suspeita"""
    test_url = {"url": "http://192.168.1.1/login-secure-bank-update"}
    response = client.post("/api/v1/predict", json=test_url)
    assert response.status_code == 200
    data = response.json()
    assert "url" in data
    assert "is_phishing" in data
    assert "confidence" in data

def test_predict_endpoint_empty_url():
    """Testa predição com URL vazia"""
    test_url = {"url": ""}
    response = client.post("/api/v1/predict", json=test_url)
    assert response.status_code == 400

def test_predict_endpoint_invalid_payload():
    """Testa predição com payload inválido"""
    response = client.post("/api/v1/predict", json={"invalid": "payload"})
    assert response.status_code == 422

def test_stats_endpoint():
    """Testa o endpoint de estatísticas"""
    response = client.get("/api/v1/stats")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "features" in data