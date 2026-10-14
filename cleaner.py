import csv

INPUT_FILE = "messy_customers.csv"
OUTPUT_FILE = "clean_customers.csv"
FIELDS = ["name", "email", "phone", "city"]

seen = set()
cleaned = []
duplicates = 0
total = 0

with open(INPUT_FILE, newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        total += 1
        name = row["name"].strip()
        email = row["email"].strip().lower()
        phone = row["phone"].strip()
        city = row["city"].strip()

        key = (name.lower(), email, phone)
        if key in seen:
            duplicates += 1
            continue
        seen.add(key)

        record = {"name": name, "email": email, "phone": phone, "city": city}
        missing = [field for field in FIELDS if not record[field]]
        record["status"] = "Valid" if not missing else "Missing " + ", ".join(missing)
        cleaned.append(record)

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=FIELDS + ["status"])
    writer.writeheader()
    writer.writerows(cleaned)

flagged = sum(1 for r in cleaned if r["status"] != "Valid")
print(f"Rows read: {total}")
print(f"Duplicates removed: {duplicates}")
print(f"Records kept: {len(cleaned)}")
print(f"Need attention: {flagged}")