# Speakeasy Lite — setup script
# Run from the repo root: .\scripts\setup.ps1

$root = Split-Path $PSScriptRoot -Parent
Set-Location $root

# ── Find Python ───────────────────────────────────────────────────────────────
$pyExe = $null
foreach ($candidate in @("python", "python3", "py")) {
    try {
        $ver = & $candidate --version 2>&1
        if ($ver -match "Python 3\.(1[1-9]|[2-9]\d)") {
            $pyExe = $candidate
            Write-Host "Using: $candidate ($ver)"
            break
        }
    } catch {}
}
if (-not $pyExe) {
    Write-Error "Python 3.11+ not found on PATH. Install from python.org and re-run."
    exit 1
}

# ── Virtual environment ───────────────────────────────────────────────────────
if (-not (Test-Path ".venv")) {
    Write-Host "Creating virtual environment..."
    & $pyExe -m venv .venv
} else {
    Write-Host "Virtual environment already exists, skipping creation."
}

# ── Install dependencies ──────────────────────────────────────────────────────
Write-Host "Installing dependencies..."
& .\.venv\Scripts\pip.exe install --upgrade pip
& .\.venv\Scripts\pip.exe install -r requirements.txt

Write-Host ""
Write-Host "Setup complete."
Write-Host "To run:   .\scripts\run.ps1"
Write-Host "To build: .\scripts\build.ps1"
