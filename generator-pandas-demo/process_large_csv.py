import csv
import tracemalloc
from pathlib import Path

CHUNK_SIZE = 100


def read_csv_in_chunks(file_path, chunk_size=CHUNK_SIZE):
    """
    Read a CSV incrementally and yield lists containing at most
    chunk_size rows. The complete CSV is never loaded into memory.
    """
    with open(file_path, "r", newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        chunk = []

        for row in reader:
            chunk.append(row)

            if len(chunk) == chunk_size:
                yield chunk
                chunk = []

        # Yield the final partial chunk, if one exists.
        if chunk:
            yield chunk


def process_chunk(rows):
    """Example business logic for one chunk."""
    successful_count = 0
    amount_total = 0.0

    for row in rows:
        if row["status"] == "SUCCESS":
            successful_count += 1
            amount_total += float(row["amount"])

    return successful_count, amount_total


def main():
    file_path = Path(__file__).with_name("large_data.csv")

    total_rows = 0
    total_successful = 0
    total_amount = 0.0
    chunk_number = 0

    # Measures Python memory allocations made while tracing is active.
    tracemalloc.start()

    for chunk in read_csv_in_chunks(file_path, chunk_size=CHUNK_SIZE):
        chunk_number += 1

        successful_count, amount_total = process_chunk(chunk)

        total_rows += len(chunk)
        total_successful += successful_count
        total_amount += amount_total

        print(
            f"Chunk {chunk_number}: "
            f"rows={len(chunk)}, "
            f"successful={successful_count}, "
            f"amount={amount_total:.2f}"
        )

        # The next loop iteration replaces the previous chunk.
        # Do not append all chunks to a master list.

    current_bytes, peak_bytes = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print("\n--- FINAL SUMMARY ---")
    print(f"Total rows processed: {total_rows}")
    print(f"Successful rows: {total_successful}")
    print(f"Successful transaction amount: {total_amount:.2f}")
    print(f"Python memory currently traced: {current_bytes / 1024:.2f} KB")
    print(f"Peak Python memory traced: {peak_bytes / 1024:.2f} KB")


if __name__ == "__main__":
    main()
