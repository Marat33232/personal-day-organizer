Set-Location -Path "$PSScriptRoot\.."

Write-Host "Останавливаем контейнеры Docker..." -ForegroundColor Yellow
docker compose stop

Write-Host "Проект умешно остановлен!" -ForegroundColor Green