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

$protectedSkillNames = @(
    "research-problem-formulation",
    "research-method-design",
    "engineering-task-decomposition",
    "targeted-knowledge-closure",
    "topic-paper-finder",
    "weekly-paper-radar",
    "vault-note-finder",
    "reading-note-builder",
    "review-note-builder",
    "systems-paper-writing",
    "hpc-paper-writing",
    "reference-validation-report"
)

$sourceRootPath = (Resolve-Path -LiteralPath $SourceRoot).Path
$requiredPaths = @(
    "explicit-skill-router\SKILL.md",
    "explicit-skill-router\aliases.yaml",
    "explicit-skill-router\agents\openai.yaml",
    "shared\scripts\enforce_explicit_skill_policy.py"
)
$requiredPaths += $protectedSkillNames | ForEach-Object { "$_\SKILL.md" }
$requiredPaths += $protectedSkillNames | ForEach-Object { "$_\agents\openai.yaml" }

foreach ($relativePath in $requiredPaths) {
    $sourcePath = Join-Path $sourceRootPath $relativePath
    if (-not (Test-Path -LiteralPath $sourcePath -PathType Leaf)) {
        throw "Missing explicit-skill policy dependency: $sourcePath"
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
            throw "Hash mismatch after explicit-skill policy sync: $targetPath"
        }
    }

    & python (Join-Path $sourceRootPath "shared\scripts\enforce_explicit_skill_policy.py") --root $targetRootPath
    if ($LASTEXITCODE -ne 0) {
        throw "Explicit-skill policy enforcement failed for $targetRootPath"
    }

    Write-Output "verified=$targetRootPath protected=$($protectedSkillNames.Count) router=1 files=$($requiredPaths.Count)"
}
