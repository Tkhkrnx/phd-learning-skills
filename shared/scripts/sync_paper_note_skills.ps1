param(
    [string]$SourceRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")),
    [string]$VaultRoot = (Join-Path $env:USERPROFILE "Documents\PHR\obsidian_phr"),
    [string[]]$TargetRoots
)

$ErrorActionPreference = "Stop"

if (-not $TargetRoots) {
    $TargetRoots = @(
        (Join-Path $env:USERPROFILE ".codex\skills"),
        (Join-Path $env:USERPROFILE ".claude\skills"),
        (Join-Path $VaultRoot ".codex\skills"),
        (Join-Path $VaultRoot ".claude\skills")
    )
}

$sourceRootPath = (Resolve-Path -LiteralPath $SourceRoot).Path
$requiredPaths = @(
    "reading-note-builder\SKILL.md",
    "reading-note-builder\scripts\build_reading_note.py",
    "review-note-builder\SKILL.md",
    "review-note-builder\scripts\build_review_note.py",
    "shared\__init__.py"
)
$requiredPaths += Get-ChildItem -LiteralPath (Join-Path $sourceRootPath "shared\obsidian") -File -Filter "*.py" |
    ForEach-Object { "shared\obsidian\$($_.Name)" }
$requiredPaths += Get-ChildItem -LiteralPath (Join-Path $sourceRootPath "shared\paperquay") -File -Filter "*.py" |
    ForEach-Object { "shared\paperquay\$($_.Name)" }

foreach ($relativePath in $requiredPaths) {
    $sourcePath = Join-Path $sourceRootPath $relativePath
    if (-not (Test-Path -LiteralPath $sourcePath -PathType Leaf)) {
        throw "Missing source dependency: $sourcePath"
    }
}

foreach ($targetRoot in $TargetRoots) {
    $targetRootPath = [System.IO.Path]::GetFullPath($targetRoot)
    New-Item -ItemType Directory -Path $targetRootPath -Force | Out-Null

    foreach ($relativePath in $requiredPaths) {
        $sourcePath = Join-Path $sourceRootPath $relativePath
        $targetPath = Join-Path $targetRootPath $relativePath
        New-Item -ItemType Directory -Path (Split-Path -Parent $targetPath) -Force | Out-Null
        Copy-Item -LiteralPath $sourcePath -Destination $targetPath -Force
    }

    foreach ($relativePath in $requiredPaths) {
        $sourcePath = Join-Path $sourceRootPath $relativePath
        $targetPath = Join-Path $targetRootPath $relativePath
        if ((Get-FileHash -LiteralPath $sourcePath -Algorithm SHA256).Hash -ne
            (Get-FileHash -LiteralPath $targetPath -Algorithm SHA256).Hash) {
            throw "Hash mismatch after sync: $targetPath"
        }
    }

    Write-Output "verified=$targetRootPath files=$($requiredPaths.Count)"
}
