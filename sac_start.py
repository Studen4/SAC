import csv
from datetime import datetime

INPUT_FILE = "input.csv"
OUTPUT_FILE = "output.csv"


def run():
    today = datetime.now().strftime("%d-%m-%Y")

    with open(INPUT_FILE, newline="", encoding="utf-8") as f:
        input_rows = list(csv.DictReader(f))

    with open(OUTPUT_FILE, newline="", encoding="utf-8") as f:
        output_rows = list(csv.DictReader(f))

    output_dict = {row["Players"]: row for row in output_rows}

    for row in input_rows:
        player = row["Players"]
        score_input = float(row["Score"])

        if player not in output_dict:
            output_dict[player] = {
                "Players": player,
                "Warn": "0",
                "Score": str(int(score_input)),
                "Date": today
            }
        else:
            warn = int(output_dict[player]["Warn"])
            current_score = float(output_dict[player]["Score"])

            if warn == 0:
                current_score += score_input
            elif warn == 1:
                current_score += score_input * 0.5
            elif warn == 2:
                pass  # нічого не додаємо

            output_dict[player]["Score"] = str(int(current_score))

    # Запис у output.csv
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Players", "Warn", "Score", "Date"])
        writer.writeheader()
        writer.writerows(output_dict.values())

    # Фінальний вивід
    print("\nFinal Results:")
    for i, row in enumerate(output_dict.values(), 1):
        print(f"{i}. {row['Players']} {row['Score']}")
