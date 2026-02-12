import socket
import json
import time
import csv

HOST = "0.0.0.0"
PORT = 5005
TEST_DURATION = 10  # sekundy

OUTPUT_FILE = "data/result_imu/raw/imu_session_live.csv"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))
sock.settimeout(1.0)

print("Recording UDP IMU data...")

start_time = time.time()

with open(OUTPUT_FILE, mode="w", newline="") as file:
    writer = csv.writer(file)

    # header
    writer.writerow([
        "recv_time",
        "ts",
        "imu0_ax","imu0_ay","imu0_az",
        "imu0_gx","imu0_gy","imu0_gz",
        "imu1_ax","imu1_ay","imu1_az",
        "imu1_gx","imu1_gy","imu1_gz"
    ])

    packet_counter = 0

    while True:
        now = time.time()

        if now - start_time >= TEST_DURATION:
            break

        try:
            data, addr = sock.recvfrom(2048)
        except socket.timeout:
            continue

        recv_time = time.time()

        try:
            packet = json.loads(data.decode())
        except json.JSONDecodeError:
            continue

        writer.writerow([
            recv_time,
            packet["ts"],
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
            packet["imu1"]["gz"]
        ])

        packet_counter += 1

print(f"\nSaved {packet_counter} packets to {OUTPUT_FILE}")
sock.close()
