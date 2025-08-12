Write-Host "Iniciando PhishGuard API..." -ForegroundColor Green
Set-Location "c:\Users\Kaio vittor\Documents\PhishGuard-API\PhishGuard-API\back"
Write-Host "Instalando dependencias se necessario..." -ForegroundColor Yellow
& "C:/Users/Kaio vittor/Documents/PhishGuard-API/PhishGuard-API/.venv/Scripts/pip.exe" install pydantic-settings
Write-Host "Iniciando servidor..." -ForegroundColor Green
& "C:/Users/Kaio vittor/Documents/PhishGuard-API/PhishGuard-API/.venv/Scripts/uvicorn.exe" main:app --host 0.0.0.0 --port 8000 --reload
