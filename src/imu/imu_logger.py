import socket
import json
import time
import csv
import os
from datetime import datetime

# =========================
# KONFIGURACJA
# =========================
HOST = "0.0.0.0"
PORT = 5005
TEST_DURATION = 10  # sekundy nagrywania
OUTPUT_FILE = "data/result_imu/raw/imu_session_live.csv"

# =========================
# SESSION ID (unikalny)
# =========================
session_id = datetime.now().strftime("%Y%m%d_%H%M%S")

# =========================
# SOCKET UDP
# =========================
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))
sock.settimeout(1.0)

print("Recording UDP IMU data...")

start_time = time.time()

# upewniamy się że folder istnieje
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

with open(OUTPUT_FILE, mode="w", newline="") as file:
    writer = csv.writer(file)

    # HEADER – format pod analizę
    writer.writerow([
        "session_id", "sample_idx", "dt",
        "imu0_ax","imu0_ay","imu0_az","imu0_gx","imu0_gy","imu0_gz",
        "imu1_ax","imu1_ay","imu1_az","imu1_gx","imu1_gy","imu1_gz",
        "ts"
    ])

    packet_counter = 0
    previous_ts = None

    while True:
        now = time.time()
        if now - start_time >= TEST_DURATION:
            break

        try:
            data, addr = sock.recvfrom(2048)
        except socket.timeout:
            continue

        try:
            packet = json.loads(data.decode())
        except json.JSONDecodeError:
            continue

        # sprawdzamy czy pakiet ma wymagane dane
        if "ts" not in packet:
            continue
        if "imu0" not in packet or "imu1" not in packet:
            continue

        ts = packet["ts"]

        # =========================
        # LICZENIE dt (bezpieczne)
        # =========================
        if previous_ts is None:
            dt = 0.0
        else:
            raw_dt = (ts - previous_ts) / 1000.0  # ms → sekundy

            # zabezpieczenie:
            # - ujemne dt
            # - absurdalny skok (>1s)
            if raw_dt < 0 or raw_dt > 1.0:
                dt = 0.0
            else:
                dt = raw_dt

        previous_ts = ts

        # =========================
        # ZAPIS DO CSV
        # =========================
        writer.writerow([
            session_id,
            packet_counter,
            dt,
            packet["imu0"]["ax"],
            packet["imu0"]["ay"],
            packet["imu0"]["az"],
            packet["imu0"]["gx"],
            packet["imu0"]["gy"],
            packet["imu0"]["gz"],
            packet["imu1"]["ax"],
            packet["imu1"]["ay"],
            packet["imu1"]["az"],
            packet["imu1"]["gx"],
            packet["imu1"]["gy"],
            packet["imu1"]["gz"],
            ts
        ])

        packet_counter += 1

print(f"\nSaved {packet_counter} packets to {OUTPUT_FILE}")
sock.close()
