from datasets import load_dataset
import pandas as pd
import os

# ---------------------------
# 1. Setup
# ---------------------------
# Create output directory if it doesn't exist
output_folder = "evogym_exports"
os.makedirs(output_folder, exist_ok=True)

print("⏳ Loading dataset...")
# Load dataset from Hugging Face
ds = load_dataset("EvoGym/robots", "default", split="train")
df = ds.to_pandas()

# ---------------------------
# 2. Transformation Logic
# ---------------------------
def uuid_to_int_parts(uid):
    """
    Splits a UUID string (hex) by hyphens and converts 
    each part into a decimal integer.
    Example: "a-b-c-d-e" -> [int(a), int(b), int(c), int(d), int(e)]
    """
    parts = uid.split("-")
    return [int(p, 16) for p in parts]

def uid_to_int_full(uid):
    """
    Converts the entire UUID string into one massive integer.
    """
    return int(uid.replace("-", ""), 16)

print("⚙️  Processing UUIDs...")

# A. Apply the split conversion (Parts 1-5)
df["uid_int_parts"] = df["uid"].apply(uuid_to_int_parts)

# Expand the list column into 5 separate columns (uid_p1 to uid_p5)
df[["uid_p1", "uid_p2", "uid_p3", "uid_p4", "uid_p5"]] = pd.DataFrame(
    df["uid_int_parts"].tolist(), 
    index=df.index
)

# B. Apply the full integer conversion (Added this column)
df["uid_int"] = df["uid"].apply(uid_to_int_full)

# Optional: Drop the list column if you only want the separate columns
# df.drop(columns=["uid_int_parts"], inplace=True)

# ---------------------------
# 3. Export
# ---------------------------
output_filename = "evogym_robots_uid_split_with_full.csv"
output_path = os.path.join(output_folder, output_filename)

print(f"💾 Saving to {output_path}...")
df.to_csv(output_path, index=False)

print("\n🎉 Done! File saved successfully.")
print(f"Path: {output_path}")