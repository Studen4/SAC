import csv
import os
from datetime import datetime

INPUT_FILE = "input.csv"
OUTPUT_FILE = "output.csv"


def is_date_valid(date_str):
    try:
        datetime.strptime(date_str, "%d-%m-%Y")
        return True
    except ValueError:
        return False


def run():
    results = []

    # 1–2. Існування файлів
    output_exist = os.path.exists(OUTPUT_FILE)
    input_exist = os.path.exists(INPUT_FILE)

    results.append(("Output Exist", output_exist))
    results.append(("Input Exist", input_exist))

    if not (output_exist and input_exist):
        for i, (name, value) in enumerate(results, 1):
            print(f"{i}. {name} --> {value}")
        return

    # Читання CSV
    with open(INPUT_FILE, newline="", encoding="utf-8") as f:
        input_rows = list(csv.DictReader(f))

    with open(OUTPUT_FILE, newline="", encoding="utf-8") as f:
        output_rows = list(csv.DictReader(f))

    # 3. Players не числові
    players_ok = True
    for row in input_rows + output_rows:
        if row["Players"].isdigit():
            players_ok = False
            break

    results.append(("Players Valid", players_ok))

    # 4. Warn тільки 0 / 1 / 2
    warn_ok = True
    for row in output_rows:
        if row["Warn"] not in {"0", "1", "2"}:
            warn_ok = False
            break

    results.append(("Warn Valid", warn_ok))

    # 5. Score тільки числові
    score_ok = True
    for row in input_rows + output_rows:
        try:
            if float(row["Score"]) < 0:
                score_ok = False
                break
        except ValueError:
            score_ok = False
            break

    results.append(("Score Valid", score_ok))

    # 6. Date формат
    date_ok = True
    for row in output_rows:
        if not is_date_valid(row["Date"]):
            date_ok = False
            break

    results.append(("Date Valid", date_ok))

    # Вивід
    for i, (name, value) in enumerate(results, 1):
        print(f"{i}. {name} --> {value}")
