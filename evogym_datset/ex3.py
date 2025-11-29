from datasets import load_dataset
import pandas as pd
import numpy as np

# 1. Load the dataset (train split)
ds = load_dataset("EvoGym/robots", split="train")

# 2. Filter for Traverser-v0 + Genetic Algorithm
def is_traverser_ga(example):
    return (
        example["env_name"] == "Traverser-v0"
        and example["generated_by"] == "Genetic Algorithm"
    )

filtered = ds.filter(is_traverser_ga)

# 3. Convert to pandas DataFrame
df = filtered.to_pandas()

# 4. Sort by uid to create deterministic order
df_sorted = df.sort_values("uid").reset_index(drop=True)

# ---- New logic starts here ----

num_seeds = 3
max_per_seed = 750          # target per seed, matching paper
N = len(df_sorted)

# How many robots per seed we will actually use
# (can't exceed either max_per_seed or N//num_seeds)
n_per_seed = min(max_per_seed, N // num_seeds)

dfs = []
for seed in range(num_seeds):
    start = seed * n_per_seed
    end = start + n_per_seed
    group = df_sorted.iloc[start:end].copy()
    group["seed_id"] = seed
    dfs.append(group)

df_final = pd.concat(dfs, ignore_index=True)

print(f"Total robots in filtered dataset: {N}")
print(f"Using {n_per_seed} robots per seed × {num_seeds} seeds = {len(df_final)}")

# 7. Save to Excel
output_path = "evo_traverser_genetic_algorithm_seeded_750perseed.xlsx"
df_final.to_excel(output_path, index=False)

print(f"Saved {len(df_final)} rows to {output_path}")
