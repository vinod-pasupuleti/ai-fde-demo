import csv

def read_transactions(file_path):
    with open(file_path, newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            yield row


total_amount = 0
success_count = 0

for row in read_transactions("large_data.csv"):
    if row["status"] == "SUCCESS":
        total_amount += float(row["amount"])
        success_count += 1

print("Total Amount :", total_amount)
print("Success Count :", success_count)

# Advantages:
# - Reads one record at a time.
# - Doesn't load the entire CSV into memory.
# - Suitable for continuous processing.

# Python generators

# Choose when:
# - Processing very large files.
# - Building streaming pipelines.
# - Reading APIs or network streams.
# - Implementing custom record-by-record processing.