#!/bin/bash

# Check if a GIF file was provided
if [ -z "$1" ]; then
    echo "Usage: $0 <path_to_gif>"
    exit 1
fi

GIF_FILE="$1"
WIDTH=80
TMP_DIR=$(mktemp -d)

# Ensure cleanup on exit
cleanup() {
    rm -rf "$TMP_DIR"
}
trap cleanup EXIT

# Extract frames from the GIF
echo "Extracting frames from GIF..."
ffmpeg -i "$GIF_FILE" "$TMP_DIR/frame_%04d.png"

# Convert frames to ASCII art
echo "Converting frames to ASCII art..."
for img in "$TMP_DIR"/frame_*.png; do
    jp2a --width=$WIDTH --output="${img%.png}.txt" "$img"
done

# Display ASCII art frames sequentially
echo "Displaying ASCII art frames..."
while true; do
    for txt in "$TMP_DIR"/frame_*.txt; do
        clear
        cat "$txt"
        sleep 0.1
    done
done

