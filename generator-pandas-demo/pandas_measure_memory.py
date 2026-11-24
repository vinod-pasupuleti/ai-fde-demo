import pandas as pd
import tracemalloc

tracemalloc.start()

df = pd.read_csv("large_data.csv")

success_df = df[df["status"] == "SUCCESS"]

total_amount = success_df["amount"].sum()
success_count = len(success_df)

current, peak = tracemalloc.get_traced_memory()

print("Total amount:", total_amount)
print("Success count:", success_count)

print(f"Current memory: {current / 1024 / 1024:.2f} MB")
print(f"Peak memory:    {peak / 1024 / 1024:.2f} MB")

# Memory occupied by the DataFrames themselves
print(
    f"Original DataFrame memory: "
    f"{df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB"
)

print(
    f"Filtered DataFrame memory: "
    f"{success_df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB"
)

tracemalloc.stop()