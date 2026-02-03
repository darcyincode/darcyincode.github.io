# 同步文章并部署到 GitHub

Write-Host "正在同步文章..." -ForegroundColor Yellow

# 确保 source/_posts 目录存在
if (Test-Path "source\_posts") {
    Remove-Item "source\_posts\*" -Recurse -Force -ErrorAction SilentlyContinue
} else {
    New-Item -ItemType Directory -Path "source\_posts" -Force | Out-Null
}

# 从 notes 目录复制所有文件
Copy-Item -Path "C:\Users\darcy\llvm-project\notes\*" -Destination "source\_posts\" -Recurse -Force

Write-Host "文章同步完成！" -ForegroundColor Green

# 提交到 Git
Write-Host "正在提交到 GitHub..." -ForegroundColor Yellow
git add .
git commit -m "Update articles from notes: $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
git push origin main

Write-Host "部署完成！" -ForegroundColor Green
Write-Host "等待约2分钟后访问: https://darcyincode.github.io" -ForegroundColor Cyan
