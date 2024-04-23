# Connect to SharePoint Online (associated with Microsoft Teams)
Connect-PnPOnline -Url "https://yourtenant.sharepoint.com/sites/teamsitename" -UseWebLogin

# Get the file you want to rename
$file = Get-PnPFile -Url "/sites/teamsitename/Shared Documents/YourFile.docx"

# Rename the file
$newFileName = "NewFileName.docx"
Move-PnPFile -SourceUrl "/sites/teamsitename/Shared Documents/YourFile.docx" -TargetUrl "/sites/teamsitename/Shared Documents/$newFileName" -Force

# Disconnect from SharePoint Online
Disconnect-PnPOnline
