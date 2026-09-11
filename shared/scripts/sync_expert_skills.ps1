param(
    [string]$SourceRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")),
    [string]$VaultRoot = (Join-Path $env:USERPROFILE "Documents\PHR\obsidian_phr"),
    [string[]]$TargetRoots,
    [switch]$ProtocolOnly
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
    "explicit-skill-router\SKILL.md",
    "explicit-skill-router\aliases.yaml",
    "explicit-skill-router\agents\openai.yaml",
    "shared\__init__.py",
    "topic-paper-finder\SKILL.md",
    "topic-paper-finder\finder_config.yaml",
    "topic-paper-finder\scripts\topic_finder.py",
    "weekly-paper-radar\radar_config.yaml"
)
$requiredPaths += $skillNames | ForEach-Object { "$_\SKILL.md" }
$requiredPaths += $skillNames | ForEach-Object { "$_\agents\openai.yaml" }
$requiredPaths += "topic-paper-finder\agents\openai.yaml"
$requiredPaths += Get-ChildItem -LiteralPath (Join-Path $sourceRootPath "shared\expert-skill-references") -File |
    ForEach-Object { "shared\expert-skill-references\$($_.Name)" }
$requiredPaths += Get-ChildItem -LiteralPath (Join-Path $sourceRootPath "shared\search") -File |
    ForEach-Object { "shared\search\$($_.Name)" }
$requiredPaths += Get-ChildItem -LiteralPath (Join-Path $sourceRootPath "shared\obsidian") -File -Filter "*.py" |
    ForEach-Object { "shared\obsidian\$($_.Name)" }

if ($ProtocolOnly) {
    # Update the collaboration family without overwriting separately maintained tools.
    $requiredPaths = @($requiredPaths | Where-Object {
        $_ -eq "AGENT_COLLABORATION_SKILL_BLUEPRINT.md" -or
        $_ -like "explicit-skill-router\*" -or
        $_ -like "shared\expert-skill-references\*" -or
        $_ -match '^(research-problem-formulation|research-method-design|engineering-task-decomposition|targeted-knowledge-closure|topic-paper-finder)\\(SKILL\.md|agents\\openai\.yaml)$'
    })
}

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
