Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $PSScriptRoot
$payloadPath = Join-Path $root 'data\processed\seed_ingest.json'
$payload = Get-Content $payloadPath -Raw

Invoke-RestMethod -Method Post -Uri 'http://localhost:8000/api/ingest/doc' -ContentType 'application/json' -Body $payload
