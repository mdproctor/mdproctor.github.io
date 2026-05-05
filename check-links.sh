#!/bin/bash
# Build then check all internal links
cd "$(dirname "$0")"
echo "Building site..."
/opt/homebrew/opt/ruby/bin/bundle exec jekyll build --quiet

echo "Checking links..."
/opt/homebrew/opt/ruby/bin/htmlproofer ./_site \
  --disable-external \
  --ignore-files "./_site/kie-mirror" \
  --ignore-urls "/feed.xml,/sitemap.xml" \
  2>&1 | grep -E "ERROR|FAILED|htmlproofer" | head -50
