# check if uv is installed
$uvInstalled = Get-Command uv -ErrorAction SilentlyContinue
if (-not $uvInstalled) {
    # Download the latest Python 3 installer for Windows (64-bit)
    $pythonInstaller = "$env:TEMP\python-installer.exe"
    Invoke-WebRequest -Uri "https://www.python.org/ftp/python/3.12.3/python-3.12.3-amd64.exe" -OutFile $pythonInstaller

    # Run the installer silently and add Python to PATH
    Start-Process -FilePath $pythonInstaller -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1" -Wait

    # Remove the installer
    Remove-Item $pythonInstaller

    # Refresh environment variables for the current session
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

    # Verify installation
    python --version

    # Install uv using pip
    python -m pip install --upgrade pip
    python -m pip install uv

    # Verify uv installation
    uv --version
} else {
    Write-Host "uv is already installed."
}

# Check if the ctrl+alt+shift+b shortcut is set up in windows
function setup_shortcut() {
    $shortcutPath = [System.IO.Path]::Combine([Environment]::GetFolderPath("Desktop"), "ZipScript.lnk")
    if (-not (Test-Path $shortcutPath)) {
        # Path to your script
        $targetPath = "$PSScriptRoot\\zipScript.ps1"

        # Create the shortcut
        $wshShell = New-Object -ComObject WScript.Shell
        $shortcut = $wshShell.CreateShortcut($shortcutPath)
        $shortcut.TargetPath = "powershell.exe"
        $shortcut.Arguments = "-NoProfile -ExecutionPolicy Bypass -File `"$targetPath`""
        $shortcut.WorkingDirectory = $PSScriptRoot
        $shortcut.WindowStyle = 1
        $shortcut.IconLocation = "$env:SystemRoot\\System32\\WindowsPowerShell\\v1.0\\powershell.exe,0"
        $shortcut.Hotkey = "Ctrl+Alt+Shift+B"
        $shortcut.Save()
        Write-Host "Shortcut created at $shortcutPath"
    } else {
        Write-Host "Shortcut already exists at $shortcutPath"
    }
}

# run main.py
$scriptPath = "$PSScriptRoot\main.py"
if (Test-Path $scriptPath) {
    Write-Host "Running main.py..."
    & uv run $scriptPath
} else {
    Write-Host "main.py not found in the script directory."
}
