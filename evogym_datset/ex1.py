from datasets import load_dataset
import numpy as np

# Load dataset
dataset = load_dataset("EvoGym/robots")

output_file = "evogym_first900_GA_Traverser_v0.txt"

MAX = 2870
count = 0

with open(output_file, "w") as f:
    for row in dataset["train"]:

        # --- CORRECT FILTERS FOR THIS DATASET ---
        if row["env_name"] != "Traverser-v0":
            continue
        if row["generated_by"] != "Genetic Algorithm":
            continue
        # -----------------------------------------

        if count >= MAX:
            break

        runid = 1
        fitness = row["reward"]
        body = np.array(row["body"])

        # Write runid
        f.write(f"{runid}\n")

        # Write fitness
        f.write(f"{fitness}\n")

        # Write 5×5 structure (floats)
        for line in body:
            f.write(" ".join(f"{x:.6f}" for x in line) + "\n")

        f.write("\n")
        count += 1

print(f"Saved {count} entries.")
