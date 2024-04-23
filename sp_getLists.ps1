# Connect to SharePoint Online
Connect-PnPOnline -Url "https://yourtenant.sharepoint.com/sites/yoursite" -UseWebLogin

# Get available lists
$lists = Get-PnPList

# Output the list titles
foreach ($list in $lists) {
    Write-Output $list.Title
}

# Disconnect from SharePoint Online
Disconnect-PnPOnline
