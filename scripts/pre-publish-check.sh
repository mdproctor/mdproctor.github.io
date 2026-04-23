#!/bin/bash
# Pre-publish checks for articles and notes.
# Usage: ./scripts/pre-publish-check.sh <path-to-markdown-file>
# Requires ImageMagick (brew install imagemagick).

FILE="${1}"
ERRORS=0
MAX_WIDTH=900

if [ -z "$FILE" ]; then
  echo "Usage: $0 <path-to-markdown-file>"
  echo "  e.g. $0 _articles/fixing-claudes-sycophancy.md"
  exit 1
fi

if [ ! -f "$FILE" ]; then
  echo "File not found: $FILE"
  exit 1
fi

echo "Pre-publish check: $FILE"
echo ""

# --- Check 1: Code fences have language specifiers ---
echo "Code blocks:"
in_fence=0
line_num=0
fence_errors=0
while IFS= read -r line; do
  line_num=$((line_num + 1))
  if [[ "$line" =~ ^\`\`\`(.*) ]]; then
    lang="${BASH_REMATCH[1]}"
    if [ "$in_fence" -eq 0 ]; then
      in_fence=1
      lang_trimmed="$(echo "$lang" | tr -d '[:space:]')"
      if [ -z "$lang_trimmed" ]; then
        echo "  WARN line $line_num: opening fence has no language specifier"
        fence_errors=$((fence_errors + 1))
        ERRORS=$((ERRORS + 1))
      fi
    else
      in_fence=0
    fi
  fi
done < "$FILE"
[ "$fence_errors" -eq 0 ] && echo "  OK — all code fences have language specifiers"

# --- Check 2: Referenced images exist and are within size limits ---
echo ""
echo "Images:"
img_errors=0
while IFS= read -r img_path; do
  # Strip leading slash to get a repo-relative path
  local_path="${img_path#/}"
  if [ ! -f "$local_path" ]; then
    echo "  MISSING: $img_path"
    img_errors=$((img_errors + 1))
    ERRORS=$((ERRORS + 1))
  else
    width=$(identify -format "%w" "$local_path" 2>/dev/null)
    if [ -n "$width" ] && [ "$width" -gt "$MAX_WIDTH" ]; then
      echo "  TOO WIDE: $img_path (${width}px — max ${MAX_WIDTH}px) — run scripts/resize-images.sh"
      img_errors=$((img_errors + 1))
      ERRORS=$((ERRORS + 1))
    fi
  fi
done < <(grep -oE '!\[[^]]*\]\([^)]+\)' "$FILE" | grep -oE '\([^)]+\)' | tr -d '()' | grep -v '^https\?://')

[ "$img_errors" -eq 0 ] && echo "  OK — all images present and within ${MAX_WIDTH}px"

# --- Summary ---
echo ""
if [ "$ERRORS" -eq 0 ]; then
  echo "All checks passed — ready to publish."
  exit 0
else
  echo "$ERRORS issue(s) found — fix before publishing."
  exit 1
fi
