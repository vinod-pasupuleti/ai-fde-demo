import pandas as pd

total_amount = 0
success_count = 0

for chunk in pd.read_csv("large_data.csv", chunksize=10000):

    success_df = chunk[chunk["status"] == "SUCCESS"]

    total_amount += success_df["amount"].sum()
    success_count += len(success_df)

print("Total Amount:", total_amount)
print("Success Count:", success_count)

# Here, Pandas reads 10,000 rows at a time rather than loading the entire file.
# Important
# - Pandas chunking is also a memory-efficient approach.
# - You do not always need to write your own generator.


# Pandas

# Choose when:
# - Performing data analysis.
# - Filtering and aggregating tabular data.
# - Joining datasets.
# - Performing vectorized calculations.

# Q) You have a 1 TB CSV file and only 8 GB RAM. You need to filter records, calculate total sales and save the results. Which approach would you choose?
# A) Use generator-based streaming or Pandas chunksize
