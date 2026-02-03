# Deploy blog to GitHub
$notesPath = "C:\Users\darcy\llvm-project\notes"
$postsPath = "source\_posts"

Write-Host "Starting deployment..." -ForegroundColor Cyan

# Remove symlink
if (Test-Path $postsPath) {
    Remove-Item $postsPath -Recurse -Force
}

# Copy articles
Write-Host "Copying articles..." -ForegroundColor Yellow
Copy-Item -Path "$notesPath\*" -Destination $postsPath -Recurse -Force

# Commit and push
Write-Host "Pushing to GitHub..." -ForegroundColor Yellow
git add .
git commit -m "Update articles - $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
git push origin main

# Remove copied files
Remove-Item $postsPath -Recurse -Force

# Restore symlink (requires admin)
Write-Host "`nRestoring symlink..." -ForegroundColor Yellow
Start-Process powershell -Verb RunAs -ArgumentList "-Command", "cd '$PWD'; New-Item -ItemType SymbolicLink -Path '$postsPath' -Target '$notesPath'" -Wait

Write-Host "`nDeployment complete!" -ForegroundColor Green
