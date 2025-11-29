from datasets import load_dataset
import pandas as pd
import os

# Output folder (optional)
output_folder = "evogym_exports"
os.makedirs(output_folder, exist_ok=True)

# 1. Load dataset
ds = load_dataset("EvoGym/robots", "default", split="train")

# 2. Convert once to pandas
df = ds.to_pandas()

# 3. Helper: convert UUID string -> big integer
def uid_to_int(uid: str) -> int:
    return int(uid.replace("-", ""), 16)

# 4. Add numeric and string-safe representation
df["uid_int"] = df["uid"].apply(uid_to_int)
df["uid_int_str"] = df["uid_int"].astype(str)

# ---------------------------
# Export 1: Sorted by numeric UUID
# ---------------------------
df_sorted = df.sort_values("uid_int", ascending=True)

sorted_path = os.path.join(output_folder, "evogym_all_sorted.xlsx")
df_sorted.to_excel(sorted_path, index=False)
print(f"✔ Saved sorted dataset → {sorted_path}")

# ---------------------------
# Export 2: Not sorted, only transformed
# ---------------------------
unsorted_path = os.path.join(output_folder, "evogym_all_unsorted.xlsx")
df.to_excel(unsorted_path, index=False)
print(f"✔ Saved unsorted (but converted) dataset → {unsorted_path}")

print("\n🎉 Done!")
