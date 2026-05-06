#!/bin/bash
# Run locally: ./serve.sh
# Then open http://localhost:4000
cd "$(dirname "$0")"
/opt/homebrew/opt/ruby/bin/bundle exec jekyll serve --livereload --incremental --port 4000 2>&1
