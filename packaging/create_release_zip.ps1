$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
$dist = Join-Path $root "dist"
$name = "峰子分析-v1.0"
$zipPath = Join-Path $dist "$name.zip"

New-Item -ItemType Directory -Force -Path $dist | Out-Null
$stage = Join-Path $env:TEMP $name
if (Test-Path $stage) { Remove-Item $stage -Recurse -Force }
New-Item -ItemType Directory -Path $stage | Out-Null

$exclude = @(".venv", "__pycache__", ".git", "dist", "*.pyc")
Get-ChildItem $root -Force | Where-Object {
    $_.Name -notin @(".venv", "__pycache__", ".git", "dist")
} | ForEach-Object {
    Copy-Item $_.FullName -Destination $stage -Recurse -Force
}

if (Test-Path $zipPath) { Remove-Item $zipPath -Force }
Compress-Archive -Path (Join-Path $stage "*") -DestinationPath $zipPath -Force
Remove-Item $stage -Recurse -Force
Write-Host "Created: $zipPath"
