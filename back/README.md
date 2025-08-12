# PhishGuard API

API para detecção de URLs de phishing usando Machine Learning.

## 🚀 Como Iniciar a API

### Opção 1: Usando o Script Batch (Windows)
```bash
# Execute o arquivo start_api.bat
start_api.bat
```

### Opção 2: Usando PowerShell
```powershell
# Execute o script PowerShell
.\start_api.ps1
```

### Opção 3: Comandos Manuais

1. **Navegue para o diretório do backend:**
```bash
cd "c:\Users\Kaio vittor\Documents\PhishGuard-API\PhishGuard-API\back"
```

2. **Ative o ambiente virtual e inicie a API:**
```bash
# Usando uvicorn diretamente
"C:/Users/Kaio vittor/Documents/PhishGuard-API/PhishGuard-API/.venv/Scripts/uvicorn.exe" main:app --host 0.0.0.0 --port 8000 --reload

# OU usando Python
"C:/Users/Kaio vittor/Documents/PhishGuard-API/PhishGuard-API/.venv/Scripts/python.exe" main.py
```

### Opção 4: Usando pip e uvicorn
```bash
cd "c:\Users\Kaio vittor\Documents\PhishGuard-API\PhishGuard-API\back"
pip install fastapi uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## 📋 Após Iniciar a API

A API estará disponível em:
- **URL Principal:** http://localhost:8000
- **Documentação Swagger:** http://localhost:8000/docs
- **Documentação ReDoc:** http://localhost:8000/redoc

## 🔗 Endpoints Disponíveis

### 1. Verificação de Saúde
```
GET /api/v1/health
```

### 2. Predição de Phishing
```
POST /api/v1/predict
Content-Type: application/json

{
    "url": "https://exemplo.com"
}
```

### 3. Estatísticas da API
```
GET /api/v1/stats
```

## 🧪 Testando a API

### Usando curl:
```bash
# Teste de saúde
curl http://localhost:8000/api/v1/health

# Teste de predição
curl -X POST "http://localhost:8000/api/v1/predict" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://google.com"}'
```

### Usando PowerShell:
```powershell
# Teste de predição
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/predict" -Method Post -Body '{"url": "https://google.com"}' -ContentType "application/json"
```

## 🛠️ Estrutura do Projeto

```
backend/
├── app/
│   ├── api/
│   │   └── routes.py          # Endpoints da API
│   ├── core/
│   │   └── config.py          # Configurações
│   ├── models/
│   │   └── url.py             # Modelos Pydantic
│   └── services/
│       └── predictor.py       # Lógica de ML
├── ml_model/
│   └── phishing_classifier_model.pkl
├── tests/
│   └── test_api.py
├── main.py                    # Arquivo principal
├── requirements.txt           # Dependências
├── start_api.bat              # Script para Windows
└── start_api.ps1              # Script PowerShell
```

## 📊 Exemplo de Resposta

```json
{
    "url": "https://google.com",
    "is_phishing": false,
    "confidence": 0.92,
    "risk_level": "Baixo",
    "features": {
        "url_length": 18,
        "num_dots": 1,
        "num_subdomains": 0,
        "has_ip": 0.0,
        "has_suspicious_words": 0.33,
        "num_suspicious_chars": 0.0,
        "domain_age": 0.5,
        "has_https": 1,
        "url_depth": 0,
        "num_params": 0
    }
}
```

## 🔧 Solução de Problemas

### Erro de Importação do Pydantic
Se encontrar o erro `BaseSettings has been moved to the pydantic-settings package`, instale o pacote necessário:
```bash
pip install pydantic-settings
```

### Erro de Importação Geral
Se encontrar erros de importação, certifique-se de que está executando do diretório correto:
```bash
cd "c:\Users\Kaio vittor\Documents\PhishGuard-API\PhishGuard-API\back"
```

### Erro de Dependências
Se faltarem dependências, instale-as:
```bash
pip install -r requirements.txt
```

### Porta em Uso
Se a porta 8000 estiver em uso, mude para outra porta:
```bash
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

### Erro de Modelo
Se encontrar erro relacionado ao modelo de ML, o sistema usará um modelo mock para demonstração.
