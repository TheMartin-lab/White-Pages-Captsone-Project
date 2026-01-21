$ScriptPath = Split-Path -Parent $MyInvocation.MyCommand.Definition
$ProjectRoot = Split-Path -Parent $ScriptPath
$DataDir = Join-Path $ProjectRoot "local_db"

Write-Host "Starting MariaDB from: $DataDir"

# Function to check if a command exists
function Test-Command {
    param($Name)
    $Command = Get-Command $Name -ErrorAction SilentlyContinue
    return $null -ne $Command
}

$MariaDBPath = "C:\Program Files\MariaDB 12.1\bin\mysqld.exe"
if (-not (Test-Command mysqld)) {
    if (Test-Path $MariaDBPath) {
        $Env:Path += ";$(Split-Path -Parent $MariaDBPath)"
    }
}

# Check if data directory exists, if not, initialize it
if (-not (Test-Path $DataDir)) {
    Write-Host "Data directory not found. Creating and initializing new database at $DataDir..."
    New-Item -ItemType Directory -Force -Path $DataDir | Out-Null
    
    $InitCmd = "mysql_install_db.exe"
    if (-not (Test-Command $InitCmd)) {
        if (Test-Path $MariaDBPath) {
             $BinDir = Split-Path -Parent $MariaDBPath
             $InitCmd = Join-Path $BinDir "mysql_install_db.exe"
        }
    }

    if (Test-Command $InitCmd -or (Test-Path $InitCmd)) {
        & $InitCmd --datadir="$DataDir"
    } else {
        Write-Error "Cannot find mysql_install_db.exe to initialize database."
        exit 1
    }
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Database initialized."
    } else {
        Write-Error "Database initialization failed."
        exit 1
    }
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
