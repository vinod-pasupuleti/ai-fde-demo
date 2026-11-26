
import csv
import os
import time
import tracemalloc
from pathlib import Path

INPUT_FILE = Path("./large_data.csv")
OUTPUT_FILE = Path("./output/generator_output.csv")

def read_csv_generator(file_path, chunk_size=10000):
    """Read CSV incrementally and yield batches."""
    with open(file_path, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        yield reader.fieldnames, None  # Send headers first

        batch = []

        for row in reader:
            batch.append(row)

            if len(batch) >= chunk_size:
                yield None, batch
                batch = []

        if batch:
            yield None, batch


def process_csv():
    start_time = time.perf_counter()
    tracemalloc.start()

    total_records = 0
    success_count = 0
    total_amount = 0.0

    # CREATE output file and write processed records
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as output:
        batches = read_csv_generator(INPUT_FILE)

        fieldnames, _ = next(batches) # requests the first value from the generator.
        # The underscore _ means we are intentionally ignoring the second returned value.

        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()

        for _, batch in batches: # (None, [dict1, dict2, dict3, ...])

            for row in batch:
                total_records += 1

                row["status"] = row["status"].strip().upper()

                if row["status"] == "SUCCESS":
                    success_count += 1
                    total_amount += float(row["amount"])
                    writer.writerow(row)

            del batch

    current_memory, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    end_time = time.perf_counter()

    original_size = INPUT_FILE.stat().st_size
    output_size = OUTPUT_FILE.stat().st_size

    print("\n========== GENERATOR RESULTS ==========")
    print(f"Original file size: {original_size / (1024**2):.2f} MB")
    print(f"Output file size: {output_size / (1024**2):.2f} MB")
    print(f"Total records: {total_records}")
    print(f"Successful records: {success_count}")
    print(f"Total successful amount: {total_amount:.2f}")
    print(f"Current memory: {current_memory / (1024**2):.2f} MB")
    print(f"Peak memory: {peak_memory / (1024**2):.2f} MB")
    print(f"Memory released from peak: {(peak_memory-current_memory) / (1024**2):.2f} MB")
    print(f"Execution time: {end_time-start_time:.2f} seconds")


if __name__ == "__main__":
    process_csv()
