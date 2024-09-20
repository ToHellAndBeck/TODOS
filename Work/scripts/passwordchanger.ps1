#Adds active directory module
Import-Module ActiveDirectory

# Prompt for credentials
$credentials = Get-Credential -Message "Enter your domain credentials"

# Function to change user password
function Set-UserPassword {
    param (
        [Parameter(Mandatory = $true)]
        [string]$UserName,
        [Parameter(Mandatory = $true)]
        [string]$NewPassword
    )

    try {
        # Set the new password for the user
        Set-ADAccountPassword -Identity $UserName -Reset -NewPassword (ConvertTo-SecureString -AsPlainText $NewPassword -Force) -ErrorAction Stop -Credential $credentials

        # Set ChangePasswordAtLogon to true
        Set-ADUser -Identity $UserName -ChangePasswordAtLogon $true -Credential $credentials

        # Output success message
        Write-Host "Success: Password changed for $UserName" -ForegroundColor Green
        return $UserName
    }
    catch {
        # Output failure message
        Write-Host "Fail: Unable to change password for $UserName" -ForegroundColor Red
        return $null
    }
}

# Prompt for usernames
$usernames = Read-Host "Enter the usernames separated by comma"

# Prompt for new password
$newPassword = Read-Host "Enter the new password" -AsSecureString

# Convert secure string to plain text
$newPasswordText = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto([System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($newPassword))

# Convert the string of usernames to an array
$userList = $usernames -split ','

# Array to store success usernames
$successUsers = @()

# Loop through each user and change password
foreach ($user in $userList) {
    $result = Set-UserPassword -UserName $user.Trim() -NewPassword $newPasswordText
    if ($result) {
        $successUsers += $result
    }
}

# Output usernames with status
foreach ($user in $userList) {
    if ($successUsers -contains $user.Trim()) {
        Write-Host "Success: $user" -ForegroundColor Green
    } else {
        Write-Host "Fail: $user" -ForegroundColor Red
    }
}
