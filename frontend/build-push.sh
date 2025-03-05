#!/bin/bash

# Require a tag as argument
if [ -z "$1" ]; then
  echo "Error: Tag argument is required"
  echo "Usage: $0 <tag>"
  exit 1
fi

TAG=$1

# Ensure we're building from the frontend directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

docker buildx build --platform linux/amd64 -t ghcr.io/wmgeolab/scope-frontend:$TAG --push .