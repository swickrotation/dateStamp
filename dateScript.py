import os
import re
import shutil
import sys

# --- CONFIG ---
DRY_RUN = False

pattern = re.compile(
    r"(?P<day>\d{1,2})\s*(?P<month>"
    r"Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|"
    r"janv|f[eé]v|mars|avr|mai|juin|juil(let)?|ao[uû]t?|sept|oct|nov|d[eé]c"
    r")\s*(?P<year>\d{4})(?:\s*\((?P<hour>\d{2})h(?P<minute>\d{2})\))?",
    re.IGNORECASE,
)

month_map = {
    # English
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
    # French (short + long + accents. Not repeating where abbreviation is the same.)
    "janv": "01",
    "fev": "02",
    "fév": "02",
    "mars": "03",
    "avr": "04",
    "mai": "05",
    "juin": "06",
    "juil": "07",
    "juillet": "07",
    "aou": "08",
    "aoû": "08",
    "aout": "08",
    "août": "08",
    "sept": "09",
    "déc": "12",
}

# --- INPUT ---
if len(sys.argv) < 3:
    print("Usage: python dateScript.py <input_dir> <output_dir>")
    sys.exit(1)

input_dir = os.path.abspath(sys.argv[1])
output_dir = os.path.abspath(sys.argv[2])

os.makedirs(output_dir, exist_ok=True)

# --- PROCESS RECURSIVELY ---
for root, dirs, files in os.walk(input_dir):

    # Compute relative path (preserve structure)
    rel_dir = os.path.relpath(root, input_dir)
    target_dir = os.path.join(output_dir, rel_dir)

    os.makedirs(target_dir, exist_ok=True)

    for filename in files:
        src_path = os.path.join(root, filename)

        name, ext = os.path.splitext(filename)
        matches = list(pattern.finditer(name))
        match = matches[-1] if matches else None

        if match:
            day = match.group("day").zfill(2)

            month_str = match.group("month").lower()
            month = month_map.get(month_str)

            # If somehow unknown month slips through, fallback safely
            if not month:
                new_filename = filename
            else:
                year = match.group("year")

                new_date = f"{year}-{month}-{day}"

                if match.group("hour"):
                    hour = match.group("hour")
                    minute = match.group("minute")
                    new_date += f"T{hour}:{minute}"

                start, end = match.span()
                new_name_part = (name[:start] + name[end:]).strip("_- ")

                if not new_name_part:
                    new_name_part = "file"

                new_filename = f"{new_date} {new_name_part}{ext}"
        else:
            new_filename = filename

        dst_path = os.path.join(target_dir, new_filename)

        if DRY_RUN:
            print(f"[DRY RUN] {src_path} → {dst_path}")
        else:
            if os.path.exists(dst_path):
                print(f"[SKIP] Exists: {dst_path}")
                continue

            shutil.copy2(src_path, dst_path)
            print(f"Copied: {src_path} → {dst_path}")
