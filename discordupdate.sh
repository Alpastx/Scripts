#!/bin/bash
set -e
FILE="/opt/discord/resources/build_info.json"
if [[ ! -f "$FILE" ]]; then
    echo "Error: $FILE not found!"
    exit 1
fi
VERSION=$(jq -r '.version' "$FILE")
IFS='.' read -r major minor patch <<< "$VERSION"
patch=$((patch + 1))

NEW_VERSION="$major.$minor.$patch"
tmpfile=$(mktemp)
jq --arg v "$NEW_VERSION" '.version = $v' "$FILE" > "$tmpfile" && mv "$tmpfile" "$FILE"

echo "Updated version: $VERSION → $NEW_VERSION"
