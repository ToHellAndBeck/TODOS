# Define Wi-Fi profiles and VPN connection name
$GuestWiFi = "Guest of Wachter"       # Replace with the actual guest Wi-Fi name
$OriginalWiFi = "Wachter WiFi" # Replace with the original Wi-Fi name
$VPNName = "Wachter VPN"     # Replace with the actual VPN connection name
$CaptivePortalURL = "https://networkcheck.kde.org" # Replace with the actual captive portal URL

# Connect to Guest Wi-Fi
Write-Host "Connecting to Guest Wi-Fi..."
netsh wlan connect name=$GuestWiFi
Start-Sleep -Seconds 10  # Wait for the connection to establish

# Open captive portal in the default web browser
Write-Host "Opening the captive portal in your browser..."
Start-Process $CaptivePortalURL

# Pause to allow user to complete captive portal authentication
Write-Host "Please complete the captive portal authentication, then press Enter to continue..."
Read-Host

# Connect to VPN
Write-Host "Connecting to VPN..."
rasdial $VPNName
Start-Sleep -Seconds 10  # Wait for the VPN connection to establish

# Switch back to Original Wi-Fi
Write-Host "Switching back to Original Wi-Fi..."
netsh wlan connect name=$OriginalWiFi
Start-Sleep -Seconds 10  # Wait for the connection to establish

# Confirm the process is complete
Write-Host "Process complete. You should now have access to the network drive."
