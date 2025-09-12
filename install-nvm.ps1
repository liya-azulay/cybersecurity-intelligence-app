# PowerShell script to install nvm-windows
# Run as Administrator

Write-Host "🚀 Installing nvm-windows..." -ForegroundColor Green

# Check if running as Administrator
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "❌ This script must be run as Administrator!" -ForegroundColor Red
    Write-Host "Right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
    pause
    exit 1
}

# Download nvm-windows installer
$nvmUrl = "https://github.com/coreybutler/nvm-windows/releases/latest/download/nvm-setup.exe"
$nvmInstaller = "$env:TEMP\nvm-setup.exe"

Write-Host "📥 Downloading nvm-windows installer..." -ForegroundColor Blue
try {
    Invoke-WebRequest -Uri $nvmUrl -OutFile $nvmInstaller -UseBasicParsing
    Write-Host "✅ Download completed!" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to download nvm-windows installer" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    pause
    exit 1
}

# Install nvm-windows
Write-Host "🔧 Installing nvm-windows..." -ForegroundColor Blue
try {
    Start-Process -FilePath $nvmInstaller -ArgumentList "/S" -Wait
    Write-Host "✅ nvm-windows installed successfully!" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to install nvm-windows" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    pause
    exit 1
}

# Clean up installer
Remove-Item $nvmInstaller -Force

Write-Host ""
Write-Host "🎉 nvm-windows installation completed!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Next steps:" -ForegroundColor Yellow
Write-Host "1. Restart your computer" -ForegroundColor White
Write-Host "2. Open a new Command Prompt or PowerShell" -ForegroundColor White
Write-Host "3. Run: nvm install 20.18.0" -ForegroundColor White
Write-Host "4. Run: nvm use 20.18.0" -ForegroundColor White
Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

