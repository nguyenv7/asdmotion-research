param([string]$Tectonic = '')
$ErrorActionPreference = 'Stop'
$researchRoot = Split-Path -Parent $PSScriptRoot
if (-not $Tectonic) {
    $researchCompiler = Get-Command tectonic -ErrorAction SilentlyContinue
    if ($researchCompiler) { $Tectonic = $researchCompiler.Source }
    else {
        $researchBundle = Join-Path $env:USERPROFILE '.codex/plugins/cache/openai-bundled/latex'
        $researchCandidates = Get-ChildItem -LiteralPath $researchBundle -Filter tectonic.exe -Recurse -ErrorAction SilentlyContinue
        $Tectonic = ($researchCandidates | Sort-Object FullName -Descending | Select-Object -First 1).FullName
    }
}
if (-not $Tectonic -or -not (Test-Path -LiteralPath $Tectonic)) { throw 'Install Tectonic or provide -Tectonic with an existing executable path.' }
$researchOutput = Join-Path $researchRoot 'outputs/latex'
New-Item -ItemType Directory -Force -Path $researchOutput | Out-Null
Push-Location (Join-Path $researchRoot 'docs/latex')
try {
    & $Tectonic -X compile main.tex --outdir $researchOutput --untrusted --keep-logs
    if ($LASTEXITCODE -ne 0) { throw "LaTeX compilation failed: $LASTEXITCODE" }
} finally { Pop-Location }
