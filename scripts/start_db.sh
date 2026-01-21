#!/bin/bash

# Get the directory of the script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
DATA_DIR="$SCRIPT_DIR/local_db"

echo "Starting MariaDB from: $DATA_DIR"

# Check if mysqld is in PATH
if ! command -v mysqld &> /dev/null; then
    echo "Error: mysqld could not be found. Please ensure MariaDB is installed and in your PATH."
    exit 1
fi

# Start mysqld with the local data directory and port 3307
mysqld --console --datadir="$DATA_DIR" --port=3307
