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

try {
    docker info | Out-Null
} catch {
    throw "Docker engine is not reachable. Start Docker Desktop (or docker daemon) first."
}

if ($NoBuild) {
    docker compose up -d
} else {
    docker compose up --build -d
}

Write-Host 'math-sys stack started.'
Write-Host 'API docs: http://localhost:8000/docs'
Write-Host 'Web demo: http://localhost:3000'
