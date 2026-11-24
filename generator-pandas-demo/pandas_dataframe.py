import pandas as pd

df = pd.read_csv("large_data.csv")

success_df = df[df["status"] == "SUCCESS"]

total_amount = success_df["amount"].sum()
success_count = len(success_df)

print("Total Amount :", total_amount)
print("Success COunt :", success_count)