# Install SharePoint Online Management Shell module if not already installed
# Install-Module -Name Microsoft.Online.SharePoint.PowerShell -Force

# Import the SharePoint Online module
Import-Module Microsoft.Online.SharePoint.PowerShell -DisableNameChecking

# Define the service principal credentials
$clientId = "your-client-id"
$clientSecret = "your-client-secret"
$tenantId = "your-tenant-id"
$siteUrl = "https://yourtenant.sharepoint.com/sites/yoursite"

# Connect to SharePoint Online using service principal credentials
Connect-SPOService -Url $siteUrl -AppId $clientId -AppSecret $clientSecret

# Now you are connected to SharePoint Online using the service principal
# You can use SharePoint Online cmdlets to perform various tasks

# For example, list all sites in SharePoint Online
Get-SPOSite
