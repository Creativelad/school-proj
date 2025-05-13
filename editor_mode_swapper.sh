#!/bin/bash
FILE="src/main.py"

current=$(grep -Po '^\s*editormode=\K\w+' "$FILE")

if [ "$current" = "True" ]; then
    sed -i 's/^\(\s*\)editormode=True/\1editormode=False/' "$FILE"
elif [ "$current" = "False" ]; then
    sed -i 's/^\(\s*\)editormode=False/\1editormode=True/' "$FILE"
else
    echo "editormode not found or invalid format"
    exit 1
fi


