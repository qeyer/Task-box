[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'

$packageRoot = $PSScriptRoot
$sourceSkill = Join-Path $packageRoot 'skills\task-box'
$sourceAgents = Join-Path $packageRoot 'AGENTS.md'
$codexHome = Join-Path $HOME '.codex'
$skillsHome = Join-Path $codexHome 'skills'
$targetSkill = Join-Path $skillsHome 'task-box'
$targetAgents = Join-Path $codexHome 'AGENTS.md'

if (-not (Test-Path -LiteralPath $sourceSkill -PathType Container)) {
    throw "Incomplete package: missing $sourceSkill"
}

if (-not (Test-Path -LiteralPath $sourceAgents -PathType Leaf)) {
    throw "Incomplete package: missing $sourceAgents"
}

New-Item -ItemType Directory -Path $skillsHome -Force | Out-Null

if (Test-Path -LiteralPath $targetSkill) {
    $timestamp = Get-Date -Format 'yyyyMMdd-HHmmss'
    $backupSkill = Join-Path $skillsHome "task-box.backup-$timestamp"
    Move-Item -LiteralPath $targetSkill -Destination $backupSkill
    Write-Host "Backed up the previous skill: $backupSkill"
}

Copy-Item -LiteralPath $sourceSkill -Destination $targetSkill -Recurse
Write-Host "Installed skill: $targetSkill"

$sourceAgentsText = Get-Content -LiteralPath $sourceAgents -Raw -Encoding UTF8
$sectionMarker = '## ' + [char]0x4EFB + [char]0x52A1 + [char]0x6536 + [char]0x7EB3
$markerIndex = $sourceAgentsText.IndexOf($sectionMarker)

if ($markerIndex -lt 0) {
    throw 'The task-box section is missing from the packaged AGENTS.md.'
}

$taskBoxRules = $sourceAgentsText.Substring($markerIndex).Trim()

if (-not (Test-Path -LiteralPath $targetAgents -PathType Leaf)) {
    Copy-Item -LiteralPath $sourceAgents -Destination $targetAgents
    Write-Host "Installed global rules: $targetAgents"
}
else {
    $targetAgentsText = Get-Content -LiteralPath $targetAgents -Raw -Encoding UTF8

    if ($targetAgentsText.Contains($sectionMarker)) {
        Write-Host 'The task-box section already exists; no duplicate was added.'
    }
    else {
        Add-Content -LiteralPath $targetAgents -Value "`r`n`r`n$taskBoxRules`r`n" -Encoding UTF8
        Write-Host "Appended the task-box rules to: $targetAgents"
    }
}

Write-Host ''
Write-Host 'Installation complete. Restart Codex or open a new Codex session.'
