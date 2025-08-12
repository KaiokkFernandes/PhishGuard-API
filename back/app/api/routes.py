from fastapi import APIRouter, HTTPException
from app.models.url import URLItem, PredictionResponse, HealthResponse
from app.services.predictor import PhishingPredictor
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Criar router
router = APIRouter()

# Inicializar preditor
predictor = PhishingPredictor()

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Endpoint para verificar se a API está funcionando"""
    return HealthResponse(
        status="healthy",
        message="PhishGuard API está funcionando corretamente"
    )

@router.post("/predict", response_model=PredictionResponse)
async def predict_phishing(url_item: URLItem):
    """
    Analisa uma URL e retorna a probabilidade de ser phishing
    
    Args:
        url_item: Objeto contendo a URL para análise
        
    Returns:
        PredictionResponse: Resultado da análise com probabilidade e detalhes
    """
    try:
        url = url_item.url.strip()
        
        # Validação básica da URL
        if not url:
            raise HTTPException(status_code=400, detail="URL não pode estar vazia")
        
        if not (url.startswith('http://') or url.startswith('https://')):
            url = 'http://' + url
        
        # Fazer predição
        is_phishing, confidence, risk_level, features = predictor.predict(url)
        
        logger.info(f"Análise concluída para URL: {url} - Phishing: {is_phishing}, Confiança: {confidence:.2f}")
        
        return PredictionResponse(
            url=url,
            is_phishing=is_phishing,
            confidence=confidence,
            risk_level=risk_level,
            features=features
        )
        
    except Exception as e:
        logger.error(f"Erro ao processar URL {url_item.url}: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Erro interno do servidor: {str(e)}"
        )

@router.get("/stats")
async def get_stats():
    """Endpoint para estatísticas da API"""
    return {
        "message": "PhishGuard API - Detecção de Phishing",
        "version": "1.0.0",
        "features": [
            "Análise de comprimento de URL",
            "Detecção de endereços IP",
            "Análise de palavras suspeitas",
            "Verificação de HTTPS",
            "Análise de estrutura de domínio"
        ]
    }