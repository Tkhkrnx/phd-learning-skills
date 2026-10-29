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
        (Join-Path $VaultRoot ".agents\skills"),
        (Join-Path $VaultRoot ".claude\skills")
    )
}
$sourceRootPath = (Resolve-Path -LiteralPath $SourceRoot).Path
$packageRoots = @(
    "nature-academic-search", "targeted-knowledge-closure", "engineering-task-decomposition",
    "systems-paper-writing", "hpc-paper-writing", "reference-validation-report",
    "shared\writing", "shared\search"
)
$relativePaths = @("shared\__init__.py")
foreach ($package in $packageRoots) {
    $relativePaths += Get-ChildItem -LiteralPath (Join-Path $sourceRootPath $package) -Recurse -File |
        Where-Object { $_.FullName -notmatch '[\\/](__pycache__|\.cache)[\\/]' -and $_.Extension -ne '.pyc' } |
        ForEach-Object { $_.FullName.Substring($sourceRootPath.Length + 1) }
}
foreach ($target in $TargetRoots) {
    $targetPath = [IO.Path]::GetFullPath($target)
    if ($targetPath -eq $sourceRootPath) { throw "Source root cannot be a deployment target" }
    foreach ($relative in $relativePaths) {
        $destination = Join-Path $targetPath $relative
        New-Item -ItemType Directory -Path (Split-Path -Parent $destination) -Force | Out-Null
        Copy-Item -LiteralPath (Join-Path $sourceRootPath $relative) -Destination $destination -Force
    }
    foreach ($relative in $relativePaths) {
        if ((Get-FileHash -LiteralPath (Join-Path $sourceRootPath $relative)).Hash -ne
            (Get-FileHash -LiteralPath (Join-Path $targetPath $relative)).Hash) {
            throw "Deployment hash mismatch: $targetPath\$relative"
        }
    }
    Write-Output "verified=$targetPath files=$($relativePaths.Count)"
}
