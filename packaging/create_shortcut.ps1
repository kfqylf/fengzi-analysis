$root = Split-Path -Parent $PSScriptRoot
$bat = Join-Path $root "峰子分析.bat"
$desktop = [Environment]::GetFolderPath("Desktop")
$lnk = Join-Path $desktop "峰子分析.lnk"

$wsh = New-Object -ComObject WScript.Shell
$sc = $wsh.CreateShortcut($lnk)
$sc.TargetPath = $bat
$sc.WorkingDirectory = $root
$sc.IconLocation = (Join-Path $root "assets\logo.png")
$sc.Description = "峰子分析 · US Sector Rotation"
$sc.Save()
Write-Host "Shortcut: $lnk"
