import csv
import os


OUTPUT_FILE = "Workspace/output.csv"


def run():
    if not os.path.exists(OUTPUT_FILE):
        print("Output.csv not found. Run Start first.")
        return

    try:
        with open(OUTPUT_FILE, newline="", encoding="utf-8") as csvfile:
            rows = list(csv.DictReader(csvfile))

        if not rows:
            print("Output.csv is empty.")
            return

        # Сортуємо за Score (від більшого до меншого)
        sorted_rows = sorted(
            rows,
            key=lambda r: float(r["Score"]),
            reverse=True
        )

        print("\nFinal result (ready for Discord):\n")

        for i, row in enumerate(sorted_rows, 1):
            score = float(row["Score"])
            score_display = int(score) if score.is_integer() else score
            print(f"`{i}. {row['Players']} {score_display}`")

        print("\nDone.\n")

    except Exception as e:
        print(f"Error reading output.csv: {e}")
