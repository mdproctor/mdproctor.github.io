#!/bin/bash
# Run locally: ./serve.sh
# Then open http://localhost:4000
cd "$(dirname "$0")"
uvx rustkyll serve --source . --port 4000 --incremental 2>&1
