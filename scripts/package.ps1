# Speakeasy Lite - build + compile installer
# Produces SpeakeasyLite-Setup.exe in the repo root.
# Run from repo root: .\scripts\package.ps1
#
# Prerequisite: Inno Setup 6 must be installed.
# Download free from jrsoftware.org (search "Inno Setup download").

$root = Split-Path $PSScriptRoot -Parent
Set-Location $root

$iscc = "C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
if (-not (Test-Path $iscc)) {
    Write-Error "Inno Setup 6 not found at '$iscc'. Install it first, then re-run this script."
    exit 1
}

& .\scripts\build.ps1
if (-not (Test-Path "dist\SpeakeasyLite\SpeakeasyLite.exe")) {
    Write-Error "PyInstaller build failed - aborting installer compilation."
    exit 1
}

Write-Host "Compiling installer..."
& $iscc "installer\speakeasy-lite.iss"

if (Test-Path "SpeakeasyLite-Setup.exe") {
    Write-Host ""
    Write-Host "Done: $root\SpeakeasyLite-Setup.exe"
} else {
    Write-Warning "Inno Setup may have failed - check output above."
}
