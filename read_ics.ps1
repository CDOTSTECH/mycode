# Replace 'path_to_your_file.ics' with the path to your .ics file
$fileContent = Get-Content -Path 'path_to_your_file.ics' -Raw

# Split the file content by the line breaks to separate each component
$events = $fileContent -split "BEGIN:VEVENT"

# Loop through each event in the file
foreach ($event in $events) {
    # Skip any empty lines
    if (-not [string]::IsNullOrWhiteSpace($event)) {
        # Get the event properties
        $summary = ($event -split "SUMMARY:")[1] -split "`n" | Select-Object -First 1
        $start = ($event -split "DTSTART:")[1] -split "`n" | Select-Object -First 1
        $end = ($event -split "DTEND:")[1] -split "`n" | Select-Object -First 1

        # Output the event details
        Write-Host "Summary: $summary"
        Write-Host "Start: $start"
        Write-Host "End: $end"
        Write-Host "------------------------"
    }
}
