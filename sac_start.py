import csv
from datetime import datetime

INPUT_FILE = "Workspace/input.csv"
OUTPUT_FILE = "Workspace/output.csv"


def run():
    today = datetime.now().strftime("%d-%m-%Y")

    # Читаємо input.csv
    with open(INPUT_FILE, newline="", encoding="utf-8") as f:
        input_rows = list(csv.DictReader(f))

    # Читаємо output.csv
    with open(OUTPUT_FILE, newline="", encoding="utf-8") as f:
        output_rows = list(csv.DictReader(f))

    # Перетворюємо output у словник для швидкого доступу
    output_dict = {row["Players"]: row for row in output_rows}

    # Основна логіка обробки
    for row in input_rows:
        player = row["Players"]
        score_input = float(row["Score"])

        if player not in output_dict:
            # Новий гравець
            output_dict[player] = {
                "Players": player,
                "Warn": "0",
                "Score": f"{score_input:.2f}",
                "Date": today
            }
        else:
            # Існуючий гравець
            warn = int(output_dict[player]["Warn"])
            current_score = float(output_dict[player]["Score"])

            if warn == 0:
                current_score += score_input
            elif warn == 1:
                current_score += score_input * 0.5
            elif warn == 2:
                pass  # нічого не додаємо

            output_dict[player]["Score"] = f"{current_score:.2f}"

    # Записуємо оновлений output.csv
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["Players", "Warn", "Score", "Date"]
        )
        writer.writeheader()
        writer.writerows(output_dict.values())

    # Фінальний вивід (Discord-friendly)
    print("\nFinal Results (ready for Discord):\n")

    for i, row in enumerate(output_dict.values(), 1):
        score = float(row["Score"])
        score_display = int(score) if score.is_integer() else score
        print(f"`{i}. {row['Players']} {score_display}`")
