import sys
import pandas as pd

EXPECTED_BLOCKS = 25

def prepare_edges(input_csv, output_txt):
    df = pd.read_csv(input_csv, dtype=str)

    if "Blocks" not in df.columns:
        raise SystemExit("❌ Input CSV must have a 'Blocks' column with 25 space-separated integers.")

    lines = []
    header = f"Run Value_Current_Best Current_Best {EXPECTED_BLOCKS} Value_Solution_At_Iteration Solution_At_Iteration"
    lines.append(header)

    for i in range(len(df) - 1):
        run = df.loc[i, "Run"]
        val_curr = df.loc[i, "Fitness"]
        vec_curr = df.loc[i, "Blocks"].strip()

        val_next = df.loc[i + 1, "Fitness"]
        vec_next = df.loc[i + 1, "Blocks"].strip()

        line = f"{run} {val_curr} {vec_curr} {val_next} {vec_next}"
        lines.append(line)

    with open(output_txt, "w") as f:
        f.write("\n".join(lines))

    print(f"✅ Wrote {len(lines)-1} edges to {output_txt}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python prepare_edges.py input.csv output.txt")
        sys.exit(1)
    prepare_edges(sys.argv[1], sys.argv[2])