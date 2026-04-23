import os
import re
import shutil
import sys

# --- CONFIG ---
DRY_RUN = True  # Set to True to preview changes without copying

pattern = re.compile(
    r"(?P<day>\d{1,2})(?P<month>Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)(?P<year>\d{4})(?:\s*\((?P<hour>\d{2})h(?P<minute>\d{2})\))?",
    re.IGNORECASE,
)

month_map = {
    "Jan": "01",
    "Feb": "02",
    "Mar": "03",
    "Apr": "04",
    "May": "05",
    "Jun": "06",
    "Jul": "07",
    "Aug": "08",
    "Sep": "09",
    "Oct": "10",
    "Nov": "11",
    "Dec": "12",
}

# --- INPUT DIRECTORY ---
if len(sys.argv) < 2:
    print("Usage: python dateScript.py <directory>")
    sys.exit(1)

input_dir = sys.argv[1]

if not os.path.isdir(input_dir):
    print(f"Error: '{input_dir}' is not a valid directory.")
    sys.exit(1)

# --- OUTPUT DIRECTORY ---
output_dir = os.path.join(input_dir, "renamed")
os.makedirs(output_dir, exist_ok=True)

unmatched = []

# --- PROCESS FILES ---
for filename in os.listdir(input_dir):
    filepath = os.path.join(input_dir, filename)

    # Skip directories (including the output folder itself)
    if os.path.isdir(filepath):
        continue

    name, ext = os.path.splitext(filename)
    match = pattern.search(name)

    if match:
        day = match.group("day").zfill(2)

        month_str = match.group("month").capitalize()
        month = month_map[month_str]

        year = match.group("year")

        # New date format: YYYYMMDD
        new_date = f"{year}{month}{day}"

        # Add time if present
        if match.group("hour"):
            hour = match.group("hour")
            minute = match.group("minute")
            new_date += f"-{hour}-{minute}"

        # Remove old date from name
        new_name_part = pattern.sub("", name).strip("_- ")

        new_filename = f"{new_date} {new_name_part}{ext}"
        new_path = os.path.join(output_dir, new_filename)

        if DRY_RUN:
            print(f"[DRY RUN] {filename} → {new_filename}")
        else:
            # Avoid overwriting existing files
            if os.path.exists(new_path):
                print(f"[SKIP] Already exists: {new_filename}")
                continue

            shutil.copy2(filepath, new_path)
            print(f"Copied: {filename} → {new_filename}")

    else:
        unmatched.append(filename)

# --- REPORT ---
print("\nFiles without date string:")
for f in unmatched:
    print(f)
