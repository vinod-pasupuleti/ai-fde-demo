
import pandas as pd
import time
import tracemalloc
from pathlib import Path

INPUT_FILE = Path("./large_data.csv")
OUTPUT_FILE = Path("./output/pandas_output.csv")
CHUNK_SIZE = 10000


def process_csv():
    start_time = time.perf_counter()
    tracemalloc.start()

    total_records = 0
    success_count = 0
    total_amount = 0.0

    # CREATE output file
    first_chunk = True

    for chunk in pd.read_csv(INPUT_FILE, chunksize=CHUNK_SIZE):

        total_records += len(chunk)

        # UPDATE: normalize status
        chunk["status"] = chunk["status"].str.strip().str.upper()

        # READ: filter successful records
        success_df = chunk[chunk["status"] == "SUCCESS"]

        success_count += len(success_df)
        total_amount += success_df["amount"].sum()

        # DELETE: failed records excluded
        # CREATE: append successful records to output
        success_df.to_csv(
            OUTPUT_FILE,
            mode="w" if first_chunk else "a",
            header=first_chunk,
            index=False
        )

        first_chunk = False

        del success_df
        del chunk

    current_memory, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    end_time = time.perf_counter()

    original_size = INPUT_FILE.stat().st_size
    output_size = OUTPUT_FILE.stat().st_size if OUTPUT_FILE.exists() else 0

    print("\n========== PANDAS RESULTS ==========")
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
