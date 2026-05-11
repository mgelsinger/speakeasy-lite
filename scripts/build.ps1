# Speakeasy Lite - PyInstaller build script
# Produces dist\SpeakeasyLite.exe
# Run from repo root: .\scripts\build.ps1

$root = Split-Path $PSScriptRoot -Parent
Set-Location $root

if (-not (Test-Path ".venv\Scripts\python.exe")) {
    Write-Error "Virtual environment not found. Run .\scripts\setup.ps1 first."
    exit 1
}

Write-Host "Installing PyInstaller..."
& .\.venv\Scripts\pip.exe install pyinstaller

Write-Host "Generating icon..."
& .\.venv\Scripts\python.exe scripts\make_icon.py

Write-Host "Building SpeakeasyLite..."
& .\.venv\Scripts\pyinstaller.exe `
    --noconfirm `
    --onedir `
    --windowed `
    --name "SpeakeasyLite" `
    --icon "app\assets\icon.ico" `
    --add-data "app\assets;assets" `
    --hidden-import "pystray._win32" `
    --hidden-import "PIL._tkinter_finder" `
    --hidden-import "winreg" `
    --collect-all "faster_whisper" `
    --collect-all "ctranslate2" `
    app\main.py

Write-Host ""
if (Test-Path "dist\SpeakeasyLite\SpeakeasyLite.exe") {
    Write-Host "Build successful: dist\SpeakeasyLite\SpeakeasyLite.exe"
} else {
    Write-Warning "Build may have failed - check output above."
}
