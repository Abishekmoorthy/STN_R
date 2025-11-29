import numpy as np

# Load your npz file
data = np.load("D:\\stn_r\\WALKER\\WALKER\\Paper_W-1C_Mar_25_v3\\generation_14\\structure\\0.npz")

# Loop through each array inside the npz
for key in data.files:
    # Get array
    arr = data[key]

    # Save as text file (CSV style, space separated)
    np.savetxt(f"{key}.txt", arr, fmt="%.6f")  

    print(f"Saved {key} -> {key}.txt")
