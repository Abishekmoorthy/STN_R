#!/usr/bin/env python3
"""
raw_to_stn_edges.py

Parse a raw file containing many runs in this pattern:

<run-id>
<fitness>
<5 numbers ...>
<5 numbers ...>
<5 numbers ...>
<5 numbers ...>
<5 numbers ...>

(repeated)

Output a file with header:
Run Value_Current_Best Current_Best 25 Value_Solution_At_Iteration Solution_At_Iteration

Each output row pairs consecutive blocks (i -> i+1) and writes:
run_i fitness_i <25 values of block i> fitness_{i+1} <25 values of block i+1>

By default values are rounded to integers. Use --float to keep them as floats.
"""

import sys
from pathlib import Path
import argparse

DIM = 25

def read_blocks(path):
    """Read file, return list of tuples: (run (str), fitness (str), values (list of str))"""
    lines = []
    with open(path, "r") as f:
        for raw in f:
            s = raw.strip()
            if s != "":
                lines.append(s)

    i = 0
    blocks = []
    n = len(lines)
    while i < n:
        # read run id
        run = lines[i].strip(); i += 1
        if i >= n:
            raise ValueError(f"Unexpected end of file after run {run}")
        fitness = lines[i].strip(); i += 1

        # gather following numbers until we have DIM values
        vals = []
        while len(vals) < DIM and i < n:
            parts = lines[i].split()
            # If the next line looks like a new run id (single integer) and we haven't collected any values,
            # this is likely an input format problem; but we try to continue.
            vals.extend(parts)
            i += 1

        if len(vals) != DIM:
            raise ValueError(f"Run {run}: expected {DIM} values, got {len(vals)}. Data near line {i}.")
        blocks.append( (run, fitness, vals) )

    return blocks

def write_edges(blocks, outpath, keep_float=False):
    header = "Run Value_Current_Best Current_Best 25 Value_Solution_At_Iteration Solution_At_Iteration"
    lines = [header]

    for idx in range(len(blocks)-1):
        run_i, fit_i, vals_i = blocks[idx]
        run_j, fit_j, vals_j = blocks[idx+1]

        if keep_float:
            fmt_vals_i = " ".join(str(float(x)) for x in vals_i)
            fmt_vals_j = " ".join(str(float(x)) for x in vals_j)
        else:
            # round to nearest integer
            fmt_vals_i = " ".join(str(int(round(float(x)))) for x in vals_i)
            fmt_vals_j = " ".join(str(int(round(float(x)))) for x in vals_j)

        # build row: run fit_i <25 vals_i> fit_j <25 vals_j>
        row = f"{run_i} {fit_i} {fmt_vals_i} {fit_j} {fmt_vals_j}"
        lines.append(row)

    with open(outpath, "w") as f:
        f.write("\n".join(lines) + "\n")

    print(f"Wrote {len(lines)-1} edges to '{outpath}' (header includes dimension {DIM})")

def main():
    p = argparse.ArgumentParser(description="Convert raw runs (run, fitness, 25 values) into STN edge file.")
    p.add_argument("input", help="raw input file path")
    p.add_argument("output", help="output STN file path")
    p.add_argument("--float", action="store_true", help="keep values as floats (default: round to integers)")
    args = p.parse_args()

    inp = Path(args.input)
    if not inp.exists():
        print("Input file not found:", inp)
        sys.exit(1)

    try:
        blocks = read_blocks(inp)
    except Exception as e:
        print("Error reading input:", e)
        sys.exit(1)

    if len(blocks) < 2:
        print("Need at least two blocks to create edges. Found:", len(blocks))
        sys.exit(1)

    write_edges(blocks, args.output, keep_float=args.float)

if __name__ == "__main__":
    main()