param(
    [string]$SourceRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")),
    [string]$VaultRoot = (Join-Path $env:USERPROFILE "Documents\PHR\obsidian_phr"),
    [string[]]$TargetRoots
)

$ErrorActionPreference = "Stop"

if (-not $TargetRoots) {
    $TargetRoots = @(
        (Join-Path $env:USERPROFILE ".codex\skills"),
        (Join-Path $env:USERPROFILE ".agents\skills"),
        (Join-Path $env:USERPROFILE ".claude\skills"),
        (Join-Path $VaultRoot ".codex\skills"),
        (Join-Path $VaultRoot ".claude\skills")
    )
}

$skillNames = @(
    "research-problem-formulation",
    "research-method-design",
    "engineering-task-decomposition",
    "targeted-knowledge-closure"
)

$sourceRootPath = (Resolve-Path -LiteralPath $SourceRoot).Path
$requiredPaths = @(
    "AGENT_COLLABORATION_SKILL_BLUEPRINT.md",
    "shared\__init__.py",
    "topic-paper-finder\SKILL.md",
    "topic-paper-finder\finder_config.yaml",
    "topic-paper-finder\scripts\topic_finder.py",
    "weekly-paper-radar\radar_config.yaml"
)
$requiredPaths += $skillNames | ForEach-Object { "$_\SKILL.md" }
$requiredPaths += Get-ChildItem -LiteralPath (Join-Path $sourceRootPath "shared\expert-skill-references") -File |
    ForEach-Object { "shared\expert-skill-references\$($_.Name)" }
$requiredPaths += Get-ChildItem -LiteralPath (Join-Path $sourceRootPath "shared\search") -File |
    ForEach-Object { "shared\search\$($_.Name)" }
$requiredPaths += Get-ChildItem -LiteralPath (Join-Path $sourceRootPath "shared\obsidian") -File -Filter "*.py" |
    ForEach-Object { "shared\obsidian\$($_.Name)" }

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
        $targetParent = Split-Path -Parent $targetPath
        New-Item -ItemType Directory -Path $targetParent -Force | Out-Null
        Copy-Item -LiteralPath $sourcePath -Destination $targetPath -Force
    }

    foreach ($relativePath in $requiredPaths) {
        $sourcePath = Join-Path $sourceRootPath $relativePath
        $targetPath = Join-Path $targetRootPath $relativePath
        $sourceHash = (Get-FileHash -LiteralPath $sourcePath -Algorithm SHA256).Hash
        $targetHash = (Get-FileHash -LiteralPath $targetPath -Algorithm SHA256).Hash
        if ($sourceHash -ne $targetHash) {
            throw "Hash mismatch after sync: $targetPath"
        }
    }

    Write-Output "verified=$targetRootPath files=$($requiredPaths.Count)"
}
