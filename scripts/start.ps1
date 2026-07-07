[Console]::outputEncoding = [System.Text.Encoding]::UTF8

Set-Location -Path "$PSScriptRoot\.."

Write-Host "Активируем виртуальное окружение..." -ForegroundColor Green
& ".\.venv\Scripts\Activate.ps1"

Write-Host "Запускает базу данных MySQL..." -ForegroundColor Green
docker compose up -d

Write-Host "Запускаем FastAPI бэкенд..." -ForegroundColor Green
uvicorn app.main:app --reload