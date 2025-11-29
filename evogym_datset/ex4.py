from datasets import load_dataset
import pandas as pd

# 1. Load dataset
ds = load_dataset("EvoGym/robots", "default", split="train")

# 2. Filter: Genetic Algorithm + Traverser-v0
ds_ga_traverser = ds.filter(
    lambda ex: ex["generated_by"] == "Genetic Algorithm"
               and ex["env_name"] == "Traverser-v0"
)

# 3. Convert to pandas (so we can handle big integers safely)
df = ds_ga_traverser.to_pandas()

# 4. Helper: convert UUID string -> big integer
def uid_to_int(uid: str) -> int:
    return int(uid.replace("-", ""), 16)

# 5. Create numeric column and sort by it
df["uid_int"] = df["uid"].apply(uid_to_int)

# Sort by the converted integer value (ascending)
df = df.sort_values("uid_int", ascending=True)

# 6. (Important for Excel) – also store the integer as a string to avoid precision loss
df["uid_int_str"] = df["uid_int"].astype(str)

# 7. Save to Excel
output_path = "evogym_ga_traverser_sorted.xlsx"
df.to_excel(output_path, index=False)

print(f"Done! Saved {len(df)} rows to {output_path}")
