
param(
    [string]$TemplatePath,
    [string[]]$TriggersToStart,   # Only these triggers will be updated
    [string]$OutputPath
)

# Load ARM template JSON
$json = Get-Content -Path $TemplatePath -Raw | ConvertFrom-Json -Depth 100

foreach ($resource in $json.resources) {

    # Only process ADF triggers
    if ($resource.type -eq "Microsoft.DataFactory/factories/triggers") {

        # Only update triggers explicitly listed
        if ($TriggersToStart -contains $resource.name) {

            if (-not $resource.properties) {
                $resource | Add-Member -MemberType NoteProperty -Name properties -Value (@{})
            }

            $resource.properties.runtimeState = "Started"

            Write-Host "Marked '$($resource.name)' as Started in template"
        }
    }
}

# Save updated template
if (-not $OutputPath) {
    $OutputPath = $TemplatePath
}

($json | ConvertTo-Json -Depth 100) | Set-Content -Path $OutputPath -Encoding utf8

Write-Host "Template updated: $OutputPath"
