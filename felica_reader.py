import csv
import time
import sys
from pirc522 import RFID

# CSVファイルの読み込み
def load_members(file_path):
    members = {}
    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                card_id, name, attend = row
                members[card_id] = name
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        sys.exit(1)
    return members

# FelicaカードのIDを読み取る関数
def read_card():
    rfid = RFID()
    while True:
        rfid.wait_for_tag()
        (error, data) = rfid.request()
        if not error:
            (error, uid) = rfid.anticoll()
            if not error:
                card_id = "".join([f"{x:02X}" for x in uid])
                return card_id
        time.sleep(1)

# メインループ
def main(file_path):
    members = load_members(file_path)
    print("Waiting for card...")

    while True:
        card_id = read_card()
        if card_id in members:
            print(f"Welcome, {members[card_id]}!")
        else:
            print("Unknown card.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python felica_reader.py <csv_file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    try:
        main(file_path)
    except KeyboardInterrupt:
        sys.exit()
