import csv
import tracemalloc

tracemalloc.start()

total_amount = 0
success_count = 0

def read_transactions(file_path):
    with open(file_path, newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            yield row

for row in read_transactions("large_data.csv"):
    if row["status"] == "SUCCESS":
        total_amount += float(row["amount"])
        success_count += 1

current, peak = tracemalloc.get_traced_memory()

print("Total amount:", total_amount)
print("Success count:", success_count)

print(f"Current memory: {current / 1024 / 1024:.2f} MB")
print(f"Peak memory:    {peak / 1024 / 1024:.2f} MB")

tracemalloc.stop()


# What do these values mean?
# - current: Python memory currently allocated at the measurement point.
# - peak: Highest traced Python memory allocation since tracing started.
# The generator doesn't retain every row. It processes one row, updates the totals, and moves to the next row.