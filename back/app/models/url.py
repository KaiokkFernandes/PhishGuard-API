from pydantic import BaseModel, HttpUrl
from typing import Optional

class URLItem(BaseModel):
    url: str
    
class PredictionResponse(BaseModel):
    url: str
    is_phishing: bool
    confidence: float
    risk_level: str
    features: Optional[dict] = None
    
class HealthResponse(BaseModel):
    status: str
    message: str