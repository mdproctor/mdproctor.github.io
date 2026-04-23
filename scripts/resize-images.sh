#!/bin/bash
# Resize images wider than MAX_WIDTH before publishing.
# Requires ImageMagick (brew install imagemagick).
# Usage: ./scripts/resize-images.sh [max-width]  (default: 900)

MAX_WIDTH="${1:-900}"
FOUND=0

while IFS= read -r -d '' img; do
  width=$(identify -format "%w" "$img" 2>/dev/null) || continue
  if [ "$width" -gt "$MAX_WIDTH" ]; then
    echo "Resizing $img (${width}px → ${MAX_WIDTH}px)"
    mogrify -resize "${MAX_WIDTH}x>" "$img"
    FOUND=1
  fi
done < <(find assets/images -type f \( -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" \) -print0)

if [ "$FOUND" -eq 0 ]; then
  echo "All images are within ${MAX_WIDTH}px — nothing to resize."
fi
