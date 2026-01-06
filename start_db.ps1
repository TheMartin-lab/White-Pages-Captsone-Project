$ScriptPath = Split-Path -Parent $MyInvocation.MyCommand.Definition
$DataDir = Join-Path $ScriptPath "local_db"

Write-Host "Starting MariaDB from: $DataDir"

# Function to check if a command exists
function Test-Command {
    param($Name)
    $Command = Get-Command $Name -ErrorAction SilentlyContinue
    return $null -ne $Command
}

# 1. Try to find mysqld in PATH
if (Test-Command mysqld) {
    Write-Host "Found mysqld in PATH."
    & mysqld --console --datadir="$DataDir" --port=3307
}
# 2. Try the specific path (fallback)
else {
    $MariaDBPath = "C:\Program Files\MariaDB 12.1\bin\mysqld.exe"
    if (Test-Path $MariaDBPath) {
        Write-Host "Found mysqld at $MariaDBPath."
        & $MariaDBPath --console --datadir="$DataDir" --port=3307
    }
    else {
        Write-Error "Error: MariaDB (mysqld.exe) not found in PATH or at default location ($MariaDBPath)."
        Write-Host "Please install MariaDB or add the 'bin' directory to your system PATH."
        exit 1
    }
}
