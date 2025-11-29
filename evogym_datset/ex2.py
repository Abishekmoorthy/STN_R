from datasets import load_dataset
import pandas as pd

# 1. Load the dataset (train split is the main one on HF)
ds = load_dataset("EvoGym/robots", split="train")

# 2. Filter for Traverser-v0 + Genetic Algorithm
def is_traverser_ga(example):
    return example["env_name"] == "Traverser-v0" and example["generated_by"] == "Genetic Algorithm"

filtered = ds.filter(is_traverser_ga)

# 3. Convert to pandas DataFrame
df = filtered.to_pandas()

# 4. Save to Excel
output_path = "evo_traverser_genetic_algorithm.xlsx"
df.to_excel(output_path, index=False)

print(f"Saved {len(df)} rows to {output_path}")
