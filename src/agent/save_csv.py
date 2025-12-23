import re

def save_csv(csv_string, path="data/testcase_matrix.csv"):
    # If it's already clean CSV, just write it
    with open(path, "w", encoding="utf-8") as f:
        f.write(csv_string)

    print(f"[OK] CSV saved → {path}")
