# Speakeasy Lite — run script
# Run from anywhere: .\scripts\run.ps1

$root = Split-Path $PSScriptRoot -Parent
Set-Location $root

if (-not (Test-Path ".venv\Scripts\python.exe")) {
    Write-Error "Virtual environment not found. Run .\scripts\setup.ps1 first."
    exit 1
}

# Ensure CUDA 12 runtime DLLs are on PATH (installer updates system PATH but
# existing shell sessions don't pick it up until restarted).
$cudaBin = "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.6\bin"
if ((Test-Path $cudaBin) -and ($env:PATH -notlike "*$cudaBin*")) {
    $env:PATH = "$cudaBin;$env:PATH"
}

& .\.venv\Scripts\python.exe app\main.py
