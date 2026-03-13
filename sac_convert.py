import os
import sys
import csv
import time
import cv2
import pytesseract
import re
import numpy as np
from collections import defaultdict

IMAGE_FOLDER = "Converter"
OUTPUT_INPUT = "Workspace/input.csv"

# нікнейми типу:
# Player
# Player_One
# ABC123
# Test_Name
NICK_REGEX = re.compile(r"[A-Za-z0-9_]{3,20}")


def get_base_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(__file__)


BASE_PATH = get_base_path()

pytesseract.pytesseract.tesseract_cmd = os.path.join(
    BASE_PATH,
    "Tesseract",
    "tesseract.exe"
)


def preprocess(img):

    # upscale для маленьких скрінів
    h, w = img.shape[:2]
    scale = 2000 / max(h, w)

    if scale > 1:
        img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)

    # переводимо в HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # маска для білого тексту
    lower_white = (0, 0, 180)
    upper_white = (180, 70, 255)

    mask = cv2.inRange(hsv, lower_white, upper_white)

    # прибираємо шум
    kernel = np.ones((3,3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # робимо текст чорним на білому
    result = 255 - mask

    return result


def extract_players(text):

    players = []

    for line in text.split("\n"):

        line = line.strip()

        if not line:
            continue

        matches = NICK_REGEX.findall(line)

        for m in matches:
            players.append(m)

    return players


def run():

    start_time = time.time()

    print("\nOCR Converter started\n")

    if not os.path.exists(IMAGE_FOLDER):
        print("ERROR: Converter folder not found.")
        return

    files = [
        f for f in os.listdir(IMAGE_FOLDER)
        if f.lower().endswith((".png", ".jpg", ".jpeg"))
    ]

    print(f"Images detected: {len(files)}")

    if not files:
        print("No images to process.")
        return

    scores = defaultdict(float)

    for file in files:

        print(f"\nProcessing: {file}")

        path = os.path.join(IMAGE_FOLDER, file)

        img = cv2.imread(path)

        if img is None:
            print("ERROR: Could not read image")
            continue

        processed = preprocess(img)

        text = pytesseract.image_to_string(
            processed,
            config="--psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_"
        )

        players = extract_players(text)

        print(f"Players extracted: {len(players)}")

        for i, player in enumerate(players):

            if i < 3:
                scores[player] += 1.25
            else:
                scores[player] += 1

    rows_written = 0

    with open(OUTPUT_INPUT, "w", newline="", encoding="utf-8") as f:

        writer = csv.writer(f)
        writer.writerow(["Players", "Score"])

        for player, score in sorted(scores.items()):
            writer.writerow([player, round(score, 2)])
            rows_written += 1

    elapsed = round(time.time() - start_time, 2)

    print("\n----- OCR SUMMARY -----")
    print(f"Players written to input.csv: {rows_written}")
    print(f"Processing time: {elapsed} seconds")
    print("Input.csv generated successfully.\n")
