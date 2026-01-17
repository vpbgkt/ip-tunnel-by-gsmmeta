# Build Script for .NET IP Tunnel Application
# Creates optimized single-file executable

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "IP Tunnel by GsmMeta - .NET Build Script" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Clean previous builds
Write-Host "Cleaning previous builds..." -ForegroundColor Yellow
if (Test-Path "bin") { Remove-Item -Path "bin" -Recurse -Force }
if (Test-Path "obj") { Remove-Item -Path "obj" -Recurse -Force }

# Build Release
Write-Host "`nBuilding Release configuration..." -ForegroundColor Yellow
dotnet build -c Release

if ($LASTEXITCODE -ne 0) {
    Write-Host "`n✗ Build failed!" -ForegroundColor Red
    exit 1
}

# Publish self-contained
Write-Host "`nPublishing self-contained executable..." -ForegroundColor Yellow
dotnet publish -c Release -r win-x64 --self-contained true /p:PublishSingleFile=true /p:IncludeNativeLibrariesForSelfExtract=true

if ($LASTEXITCODE -ne 0) {
    Write-Host "`n✗ Publish failed!" -ForegroundColor Red
    exit 1
}

# Get file info
$exePath = "bin\Release\net8.0-windows\win-x64\publish\IP_Tunnel_GsmMeta.exe"
if (Test-Path $exePath) {
    $file = Get-Item $exePath
    $sizeMB = [math]::Round($file.Length/1MB, 2)
    
    Write-Host "`n============================================================" -ForegroundColor Green
    Write-Host "✓ Build Completed Successfully!" -ForegroundColor Green
    Write-Host "============================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Executable: $($file.Name)" -ForegroundColor White
    Write-Host "Size: $sizeMB MB" -ForegroundColor White
    Write-Host "Path: $($file.FullName)" -ForegroundColor White
    Write-Host ""
    Write-Host "Note: Self-contained build includes .NET runtime" -ForegroundColor Cyan
    Write-Host "      For smaller size, users can install .NET 8 runtime separately" -ForegroundColor Cyan
    Write-Host ""
}
else {
    Write-Host "`n✗ Executable not found!" -ForegroundColor Red
    exit 1
}
