import re

def save_csv(raw_text, path="data/testcase_matrix.csv"):
    # Remove markdown fences
    cleaned = re.sub(r"```[a-zA-Z]*", "", raw_text)
    cleaned = cleaned.replace("```", "")

    # Remove comment lines
    cleaned = "\n".join(
        line for line in cleaned.splitlines() 
        if not line.strip().startswith("#")
    )

    # Remove empty lines
    cleaned = "\n".join(
        line for line in cleaned.splitlines() 
        if line.strip()
    )

    # Only keep rows that look like CSV (>= 3 commas)
    cleaned = "\n".join(
        line for line in cleaned.splitlines()
        if line.count(",") >= 3
    )

    # Save
    with open(path, "w", encoding="utf-8") as f:
        f.write(cleaned)

    print(f"[OK] CSV saved → {path}")
