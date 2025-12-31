
<#
.SYNOPSIS
Updates properties.runtimeState for selected ADF triggers in an ARM template JSON.

.DESCRIPTION
- Targets resources of type 'Microsoft.DataFactory/factories/triggers'.
- Selects triggers by exact names (-Triggers) or wildcard patterns (-IncludePatterns, -ExcludePatterns).
- Writes back to the same file (in-place) or a different -OutputPath.

.PARAMETER TemplatePath
Path to the ARM template JSON file.

.PARAMETER RuntimeState
Desired runtime state: 'Started' or 'Stopped' (metadata/intent only).

.PARAMETER Triggers
Exact trigger names to update (array). Optional.

.PARAMETER IncludePatterns
Wildcard patterns to include (e.g., 'trg_*', '*prod*'). Optional.

.PARAMETER ExcludePatterns
Wildcard patterns to exclude (e.g., '*adhoc*'). Optional.

.PARAMETER OutputPath
Optional path to save the updated template; defaults to overwriting TemplatePath.

.EXAMPLES
# Set intent to Started for two exact triggers
.\Update-AdfArmTriggerIntent.ps1 -TemplatePath .\adf\arm_template.json `
  -RuntimeState Started -Triggers "trg_daily","trg_hourly"

# Stop all triggers matching pattern except adhoc
.\Update-AdfArmTriggerIntent.ps1 -TemplatePath .\adf\arm_template.json `
  -RuntimeState Stopped -IncludePatterns "trg_*" -ExcludePatterns "*adhoc*"

# Write to a new file
.\Update-AdfArmTriggerIntent.ps1 -TemplatePath .\adf\arm_template.json `
  -RuntimeState Started -IncludePatterns "*prod*" -OutputPath .\out\arm_template.updated.json
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)]
    [string]$TemplatePath,

    [Parameter(Mandatory=$true)]
    [ValidateSet('Started','Stopped')]
    [string]$RuntimeState,

    [string[]]$Triggers,          # Exact names
    [string[]]$IncludePatterns,   # Wildcards
    [string[]]$ExcludePatterns,   # Wildcards
    [string]$OutputPath
)

if (-not (Test-Path -Path $TemplatePath)) {
    throw "Template path '$TemplatePath' not found."
}

# Load JSON with deep depth to preserve nested objects
$json = Get-Content -Path $TemplatePath -Raw | ConvertFrom-Json -Depth 100

if (-not $json.resources) {
    throw "No 'resources' array found in template. Is this an ARM template?"
}

function Test-MatchAnyPattern {
    param([string]$Text, [string[]]$Patterns)
    if (-not $Patterns -or $Patterns.Count -eq 0) { return $false }
    foreach ($p in $Patterns) {
        if ($Text -like $p) { return $true }
    }
    return $false
}

# Gather all trigger resources
$triggerResources = @()
foreach ($r in $json.resources) {
    if ($r.type -eq 'Microsoft.DataFactory/factories/triggers') {
        $triggerResources += $r
    }
}

if ($triggerResources.Count -eq 0) {
    Write-Warning "No ADF trigger resources found in template."
}

# Compute selection
$selected = @()
foreach ($r in $triggerResources) {
    $name = $r.name

    $includeByExact = ($Triggers -and ($Triggers -contains $name))
    $includeByPattern = Test-MatchAnyPattern -Text $name -Patterns $IncludePatterns
    $isIncluded = $includeByExact -or $includeByPattern

    # If neither exact nor include patterns provided, skip
    if (-not $Triggers -and -not $IncludePatterns) { $isIncluded = $false }

    # Apply exclusions
    if ($isIncluded -and (Test-MatchAnyPattern -Text $name -Patterns $ExcludePatterns)) {
        $isIncluded = $false
    }

    if ($isIncluded) { $selected += $r }
}

if ($selected.Count -eq 0) {
    Write-Warning "No triggers matched the selection. Provide -Triggers or -IncludePatterns (optionally -ExcludePatterns)."
    return
}

Write-Host "Updating $($selected.Count) trigger(s): $($selected | ForEach-Object { $_.name } -join ', ')"

# Update runtimeState for selected triggers
foreach ($r in $selected) {
    if (-not $r.properties) {
        # Ensure properties exists to place runtimeState
        $r | Add-Member -MemberType NoteProperty -Name properties -Value (@{})
    }
    $r.properties.runtimeState = $RuntimeState
}

# Save output
if (-not $OutputPath) { $OutputPath = $TemplatePath }
($json | ConvertTo-Json -Depth 100) | Set-Content -Path $OutputPath -Encoding UTF8

Write-Host "Saved updated template to: $OutputPath"
