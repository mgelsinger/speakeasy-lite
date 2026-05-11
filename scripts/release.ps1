# Speakeasy Lite - build and publish a GitHub release
# Usage: .\scripts\release.ps1 -Version v1.0.0
# Requires: gh CLI authenticated, Inno Setup 6 installed

param(
    [Parameter(Mandatory)]
    [string]$Version
)

if ($Version -notmatch '^v\d+\.\d+\.\d+$') {
    Write-Error "Version must be in the form v1.2.3 (got: $Version)"
    exit 1
}

$env:PATH = "C:\Program Files\Git\cmd;C:\Program Files\GitHub CLI;" + $env:PATH
$root = Split-Path $PSScriptRoot -Parent
Set-Location $root

# 1. Build the installer
& .\scripts\package.ps1
if (-not (Test-Path "SpeakeasyLite-Setup.exe")) {
    Write-Error "Build failed - aborting release."
    exit 1
}

# 2. Tag the commit
git tag $Version
if ($LASTEXITCODE -ne 0) {
    Write-Error "git tag failed - does $Version already exist?"
    exit 1
}
git push origin $Version

# 3. Create the GitHub release and attach the installer
$notes = "Speakeasy Lite $Version`n`nRequires an NVIDIA GPU with recent drivers.`nWhisper model (~1.5 GB) downloads automatically on first launch."
gh release create $Version "SpeakeasyLite-Setup.exe" `
    --title "Speakeasy Lite $Version" `
    --notes $notes `
    --repo mgelsinger/speakeasy-lite

Write-Host ""
Write-Host "Release published: https://github.com/mgelsinger/speakeasy-lite/releases/tag/$Version"
