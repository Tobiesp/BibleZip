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