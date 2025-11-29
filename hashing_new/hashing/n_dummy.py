import sys
import pandas as pd

def filter_columns(input_txt, output_txt):
    # Read the file as tab-delimited
    df = pd.read_csv(input_txt, sep="\t", dtype=str)

    # Keep only the first 3 columns
    df_out = df.iloc[:, :3]

    # Write back as tab-delimited
    df_out.to_csv(output_txt, sep="\t", index=False)

    print(f"✅ Wrote {output_txt} with only first 3 columns")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python filter_columns.py input.txt output.txt")
        sys.exit(1)
    filter_columns(sys.argv[1], sys.argv[2])