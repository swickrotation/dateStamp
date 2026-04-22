import os
import re
import shutil
import sys

# --- CONFIG ---
DRY_RUN = False  # Set to True to preview changes without copying

pattern = re.compile(
    r"(?P<day>\d{1,2})(?P<month>"
    r"Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|"
    r"janv|f[eé]v|mars|avr|mai|juin|juil|ao[uû]|sept|oct|nov|d[eé]c"
    r")(?P<year>\d{4})(?:\s*\((?P<hour>\d{2})h(?P<minute>\d{2})\))?",
    re.IGNORECASE,
)

month_map = {
    # If in English
    "jan": "01",
    "feb": "02",
    "mar": "03",
    "apr": "04",
    "may": "05",
    "jun": "06",
    "jul": "07",
    "aug": "08",
    "sep": "09",
    "oct": "10",
    "nov": "11",
    "dec": "12",
    # If in French
    "janv": "01",
    "fev": "02",
    "fév": "02",
    "mars": "03",
    "avr": "04",
    "mai": "05",
    "juin": "06",
    "juil": "07",
    "aou": "08",
    "aoû": "08",
    "sept": "09",
    "oct": "10",
    "nov": "11",
    "dec": "12",
    "déc": "12",
}

if len(sys.argv) < 3:
    print("Usage: python dateScript.py <input_dir> <output_dir>")
    sys.exit(1)

input_dir = sys.argv[1]
output_dir = sys.argv[2]

if not os.path.isdir(input_dir):
    print(f"Error: '{input_dir}' is not a valid directory.")
    sys.exit(1)

os.makedirs(output_dir, exist_ok=True)

unmatched = []

# --- PROCESS FILES ---

for filename in os.listdir(input_dir):
    filepath = os.path.join(input_dir, filename)

    if os.path.isdir(filepath):
        continue

    name, ext = os.path.splitext(filename)
    match = pattern.search(name)

    if match:
        day = match.group("day").zfill(2)

        month_str = match.group("month").lower()
        month = month_map[month_str]

        year = match.group("year")

        new_date = f"{year}{month}{day}"

        if match.group("hour"):
            hour = match.group("hour")
            minute = match.group("minute")
            new_date += f"-{hour}-{minute}"

        new_name_part = pattern.sub("", name).strip("_- ")

        if not new_name_part:
            new_name_part = "file"

        new_filename = f"{new_date} {new_name_part}{ext}"
    else:
        # keep original name if no match
        new_filename = filename
        unmatched.append(new_filename)

    new_path = os.path.join(output_dir, new_filename)

    if DRY_RUN:
        print(f"[DRY RUN] {filename} → {new_filename}")
    else:
        if os.path.exists(new_path):
            print(f"[SKIP] Already exists: {new_filename}")
            continue

        shutil.copy2(filepath, new_path)
        print(f"Copied: {filename} → {new_filename}")

# --- REPORT ---
print("\nFiles without date string:")
for f in unmatched:
    print(f)
