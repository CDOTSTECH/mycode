
# Simple script to update runtimeState for selected ADF triggers in ARM template

param(
    [string]$TemplatePath,          # Path to ARM template JSON
    [string[]]$TriggersToUpdate,    # Trigger names to update
    [string]$RuntimeState,          # Started or Stopped
    [string]$OutputPath             # Optional output file
)

# Load JSON
$json = Get-Content -Path $TemplatePath -Raw | ConvertFrom-Json -Depth 100

foreach ($resource in $json.resources) {
    if ($resource.type -eq "Microsoft.DataFactory/factories/triggers") {

        # Update only selected triggers
        if ($TriggersToUpdate -contains $resource.name) {

            if (-not $resource.properties) {
                $resource | Add-Member -MemberType NoteProperty -Name properties -Value (@{})
            }

            $resource.properties.runtimeState = $RuntimeState
            Write-Host "Updated trigger '$($resource.name)' to state '$RuntimeState'"
        }
    }
}

# Save back to file
if (-not $OutputPath) {
    $OutputPath = $TemplatePath
}

($json | ConvertTo-Json -Depth 100) | Set-Content -Path $OutputPath -Encoding UTF8

Write-Host "Saved updated template to $OutputPath"
