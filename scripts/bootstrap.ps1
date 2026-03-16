param(
    [switch]$NoBuild
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

if (-not (Test-Path '.env')) {
    Copy-Item '.env.example' '.env'
    Write-Host 'Created .env from .env.example'
}

if ($NoBuild) {
    docker compose up -d
} else {
    docker compose up --build -d
}

Write-Host 'math-sys stack started. Open http://localhost:8000/docs'
