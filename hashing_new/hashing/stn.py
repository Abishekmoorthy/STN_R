#!/usr/bin/env python3
"""
binblocks_to_singlecell.py

Reads input CSV with columns: Run,Fitness,Solution
Each Solution must contain exactly 25 blocks of 32-bit binary (whitespace separated).

Outputs a CSV with columns:
Run, Fitness, Blocks

Where Blocks is a single cell containing 25 integers separated by single spaces.
"""

import sys
import pandas as pd

EXPECTED_BLOCKS = 25
BITS_PER_BLOCK = 32
UINT32_MAX = 2**32
INT32_SIGN = 2**31

def bin32_to_signed_int(bstr: str) -> int:
    b = bstr.strip()
    if len(b) != BITS_PER_BLOCK:
        raise ValueError(f"binary block length {len(b)} != {BITS_PER_BLOCK}: '{b}'")
    u = int(b, 2)
    return u - UINT32_MAX if u >= INT32_SIGN else u

def convert_solution_to_spacejoined(solution_field: str) -> str:
    parts = solution_field.strip().split()
    if len(parts) != EXPECTED_BLOCKS:
        raise ValueError(f"Expected {EXPECTED_BLOCKS} blocks, got {len(parts)}")
    ints = [str(bin32_to_signed_int(p)) for p in parts]
    return " ".join(ints)

def main(infile: str, outfile: str):
    df = pd.read_csv(infile, dtype=str)  # read as strings to avoid surprises
    required_cols = {"Run", "Fitness", "Solution"}
    if not required_cols.issubset(set(df.columns)):
        raise SystemExit(f"Input CSV must contain columns: {', '.join(required_cols)}")

    out_rows = []
    for idx, row in df.iterrows():
        run = row["Run"]
        fitness = row["Fitness"]
        solution = row["Solution"]
        try:
            blocks_cell = convert_solution_to_spacejoined(solution)
        except Exception as e:
            raise SystemExit(f"Error at input row {idx+1} (Run={run}): {e}")
        out_rows.append({"Run": run, "Fitness": fitness, "Blocks": blocks_cell})

    df_out = pd.DataFrame(out_rows, columns=["Run", "Fitness", "Blocks"])
    df_out.to_csv(outfile, index=False)
    print(f"Wrote {len(df_out)} rows to {outfile}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python binblocks_to_singlecell.py input.csv output.csv")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])