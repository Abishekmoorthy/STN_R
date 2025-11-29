import numpy as np
from datasets import load_dataset

def format_and_print_data():
    print("Loading dataset...")
    # Load the dataset
    dataset = load_dataset("EvoGym/robots", split="train")
    
    print(f"Available columns: {dataset.column_names}")

    # FIXED: Prioritize 'body' since that is the correct column name in your output
    if 'body' in dataset.column_names:
        body_key = 'body'
    elif 'robot' in dataset.column_names:
        body_key = 'robot'
    else:
        body_key = 'structure'

    print(f"Using column '{body_key}' for robot structure.")
    
    # Define other keys
    reward_key = 'reward' if 'reward' in dataset.column_names else 'fitness'
    # We'll use 'generated_by' or 'uid' as the Run ID to give you distinct IDs
    run_id_key = 'generated_by' if 'generated_by' in dataset.column_names else 'uid'

    # Open a file to save the results
    with open("evogym_data_split.txt", "w") as f:
        for index, item in enumerate(dataset):
            # Limit for testing (remove this 'if' line to process all 90k lines)
            # if index >= 10: break 
            
            # 1. Get Run ID (Use 'generated_by' or fall back to index)
            run_id = item.get(run_id_key, index)
            
            # 2. Get Reward
            reward = item.get(reward_key, 0.0)
            
            # 3. Get Body and Fix Shape
            body_data = item.get(body_key)
            
            # Safety check: if body is None, skip
            if body_data is None:
                continue

            body = np.array(body_data)

            # RESHAPE LOGIC: If data is flat (25,), reshape to (5,5)
            if len(body.shape) == 1:
                side = int(np.sqrt(body.shape[0])) # usually 5
                body = body.reshape((side, side))
            
            # Get dimensions
            rows, cols = body.shape

            # --- WRITE TO FILE ---
            f.write(f"{run_id}\n")
            f.write(f"{reward}\n")
            
            for r in range(rows):
                # Format as floats with 6 decimal places
                row_str = " ".join([f"{float(val):.6f}" for val in body[r]])
                f.write(f"{row_str}\n")

    print("Done! Data saved to 'evogym_data_split.txt'")

if __name__ == "__main__":
    format_and_print_data()