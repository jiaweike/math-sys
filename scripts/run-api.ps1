Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $PSScriptRoot
Set-Location (Join-Path $root 'apps\api')

python -m venv .venv
.\.venv\Scripts\python -m pip install --upgrade pip
.\.venv\Scripts\pip install -r requirements.txt

$env:DATABASE_URL = $env:DATABASE_URL -ne $null ? $env:DATABASE_URL : 'sqlite:///./local.db'
$env:SEED_ON_START = 'true'

.\.venv\Scripts\uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
