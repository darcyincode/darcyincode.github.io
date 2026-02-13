# Deploy blog to GitHub
Write-Host "Starting deployment..." -ForegroundColor Cyan

# Commit and push
Write-Host "Committing changes..." -ForegroundColor Yellow
git add .
git commit -m "Update articles - $(Get-Date -Format 'yyyy-MM-dd HH:mm')"

Write-Host "Pushing to GitHub..." -ForegroundColor Green
git push origin main

Write-Host "`nDeployment complete!" -ForegroundColor Green
