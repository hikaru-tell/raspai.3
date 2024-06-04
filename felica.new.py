import csv
import time
import sys
from ctypes import *

# libpafe.hの77行目で定義
FELICA_POLLING_ANY = 0xffff

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
def read_card_Felica():
    libpafe = cdll.LoadLibrary("/usr/local/lib/libpafe.so")
    libpafe.pasori_open.restype = c_void_p
    libpafe.felica_polling.restype = c_void_p
    libpafe.felica_get_idm.restype = c_void_p

    pasori = libpafe.pasori_open()
    if pasori is None or pasori == 0:
        print("Pasoriが見つかりません。")
        sys.exit(1)

    libpafe.pasori_init(pasori)
    
    while True:
        felica = libpafe.felica_polling(pasori, FELICA_POLLING_ANY, 0, 0)
        if felica:
            idm = c_ulonglong()
            libpafe.felica_get_idm(felica, byref(idm))
            if idm.value != 0:
                libpafe.free(felica)
                return f"{idm.value:016X}"
        time.sleep(1)

# メインループ
def main(file_path):
    members = load_members(file_path)
    print("Waiting for card...")

    while True:
        card_id = read_card_Felica()
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
