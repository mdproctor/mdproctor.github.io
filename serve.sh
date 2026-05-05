#!/bin/bash
# Run locally: ./serve.sh
# Then open http://localhost:4000
cd "$(dirname "$0")"
/opt/homebrew/opt/ruby/bin/bundle exec jekyll serve --livereload --open-url 2>&1
