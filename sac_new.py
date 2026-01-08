import csv

OUTPUT_FILE = "output.csv"


def run():
    headers = ["Players", "Warn", "Score", "Date"]

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)

    print("New output.csv created successfully.")
