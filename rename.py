import os
from pathlib import Path

# How many digits for numbering (e.g., 4 = 0001.jpg)
PAD_LENGTH = 4

# Get all files in the current directory (excluding folders and this script)
folder = Path(__file__).resolve().parent
files = [f for f in folder.iterdir() if f.is_file() and f.name != Path(__file__).name]

# Sort files by last modified time (change to .name for alphabetical)
files.sort(key=lambda f: f.stat().st_mtime)

# First pass: rename to temp names to avoid collisions
temp_files = []
for idx, f in enumerate(files, 1):
    temp_name = folder / f"temp_ren_{idx}{f.suffix}"
    f.rename(temp_name)
    temp_files.append(temp_name)

# Second pass: rename to final names like 0001.jpg
for idx, f in enumerate(sorted(temp_files), 1):
    new_name = folder / f"{str(idx).zfill(PAD_LENGTH)}{f.suffix}"
    f.rename(new_name)

print("✅ All files renamed successfully.")
