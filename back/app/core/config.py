from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Configurações da aplicação"""
    
    # Configurações da API
    app_name: str = "PhishGuard API"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Configurações do servidor
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Configurações de CORS
    allow_origins: list = ["*"]
    allow_credentials: bool = True
    allow_methods: list = ["*"]
    allow_headers: list = ["*"]
    
    # Configurações do modelo
    model_path: str = "ml_model/phishing_classifier_model.pkl"
    
    # Configurações de logging
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"

# Instância global das configurações
settings = Settings()