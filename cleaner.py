import csv
import sys
from pathlib import Path

if len(sys.argv) != 2:
    print("CleanMyData needs one thing: the CSV file you want to clean.")
    print("")
    print("How to use it:")
    print("  python cleaner.py your_file.csv")
    print("")
    print("Your file must have a header row. That is the first row,")
    print("which names each column, e.g. name, city, email,phone, id")
    print("")
    print("The column names can be anything. This works with any CSV.")
    sys.exit(1)

input_path = Path(sys.argv[1])
if not input_path.exists():
    print(f"File not found: {input_path}")
    sys.exit(1)

output_path = input_path.with_name(input_path.stem + "_clean.csv")
STATUS = "cleaning_status"

seen = set()
cleaned = []
duplicates = 0
total = 0

with open(input_path, newline="", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    if not reader.fieldnames:
        print("This file looks empty. It needs a header row and some data.")
        sys.exit(1)

    columns = [c.strip() for c in reader.fieldnames]
    reader.fieldnames = columns
    email_cols = [c for c in columns if "mail" in c.lower()]

    for row in reader:
        total += 1
        record = {}
        for col in columns:
            value = (row.get(col) or "").strip()
            if col in email_cols:
                value = value.lower()
            record[col] = value

        key = tuple(v.lower() for v in record.values())
        if key in seen:
            duplicates += 1
            continue
        seen.add(key)

        missing = [c for c in columns if not record[c]]
        record[STATUS] = "Valid" if not missing else "Missing " + ", ".join(missing)
        cleaned.append(record)

with open(output_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=columns + [STATUS])
    writer.writeheader()
    writer.writerows(cleaned)

flagged = sum(1 for r in cleaned if r[STATUS] != "Valid")
print(f"Columns found: {', '.join(columns)}")
print(f"Rows read: {total}")
print(f"Duplicates removed: {duplicates}")
print(f"Records kept: {len(cleaned)}")
print(f"Need attention: {flagged}")
print(f"Saved to: {output_path}")