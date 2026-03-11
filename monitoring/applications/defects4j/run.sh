#!/bin/bash

# Script to handle defects4j operations with three command line arguments
# Usage: ./run.sh <project> <version_type> <defect_class> <defect_id>

# Check if exactly 4 arguments are provided
if [ $# -ne 4 ]; then
    echo "Error: This script requires exactly 4 arguments"
    echo "Usage: $0 <project> <version_type> <defect_class> <defect_id>"
    echo "Example: $0 Chart buggy order 22"
    exit 1
fi

# Assign command line arguments to variables
PROJECT="$1"
VERSION_TYPE="$2"
DEFECT_CLASS="$3"
DEFECT_ID="$4"

# Validate version type
if [[ "$VERSION_TYPE" != "buggy" && "$VERSION_TYPE" != "fixed" ]]; then
    echo "Error: VERSION_TYPE must be either 'buggy' or 'fixed'"
    echo "Received: $VERSION_TYPE"
    exit 1
fi

# Display received arguments
echo "Processing defects4j with the following parameters:"
echo "Project: $PROJECT"
echo "Defect Class: $DEFECT_CLASS"
echo "Defect ID: $DEFECT_ID"
echo "Version Type: $VERSION_TYPE"

# Determine version suffix for defects4j
if [ "$VERSION_TYPE" = "buggy" ]; then
    VERSION_SUFFIX="b"
else
    VERSION_SUFFIX="f"
fi

# Create working directory
WORK_DIR="/tmp/defects4j/${PROJECT}_${DEFECT_ID}_${DEFECT_CLASS}_${VERSION_TYPE}"
echo "Working directory: $WORK_DIR"

# Run defects4j test
echo "Running test for project $PROJECT defect $DEFECT_ID - $DEFECT_CLASS ($VERSION_TYPE version)..."
/tmp/defects4j/defects4j/framework/bin/defects4j test -w "$WORK_DIR" -r