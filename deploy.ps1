# Deploy blog to GitHub
$notesPath = "C:\Users\jike4\llvm-project\notes"
$postsPath = "source\_posts"

Write-Host "Starting deployment..." -ForegroundColor Cyan

# Remove junction/symlink
if (Test-Path $postsPath) {
    Write-Host "Removing existing junction..." -ForegroundColor Yellow
    # 使用 cmd 命令删除 junction，避免递归删除目标目录
    cmd /c "rmdir `"$postsPath`""
}

# Copy articles
Write-Host "Copying articles..." -ForegroundColor Yellow
New-Item -ItemType Directory -Path $postsPath -Force | Out-Null
Copy-Item -Path "$notesPath\*" -Destination $postsPath -Recurse -Force

# Commit and push
Write-Host "Committing changes..." -ForegroundColor Yellow
git add .
git commit -m "Update articles - $(Get-Date -Format 'yyyy-MM-dd HH:mm')"

Write-Host "Pushing to GitHub..." -ForegroundColor Green
git push origin main

# Remove copied files
Write-Host "Cleaning up..." -ForegroundColor Yellow
Remove-Item $postsPath -Recurse -Force

# Restore junction (不需要管理员权限)
Write-Host "Restoring junction..." -ForegroundColor Yellow
New-Item -ItemType Junction -Path $postsPath -Target $notesPath | Out-Null

Write-Host "`nDeployment complete! Junction restored." -ForegroundColor Green
