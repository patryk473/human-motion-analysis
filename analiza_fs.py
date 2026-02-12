import socket
import json
import time

HOST = "0.0.0.0"
PORT = 5005
TEST_DURATION = 10  # sekundy testu

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))
sock.settimeout(1.0)

print(f"Listening on {HOST}:{PORT}")
print(f"Test duration: {TEST_DURATION} seconds\n")

start_time = time.time()
last_time = None
packet_counter = 0

while True:
    now = time.time()

    # ⏹ Zatrzymaj po określonym czasie
    if now - start_time >= TEST_DURATION:
        break

    try:
        data, addr = sock.recvfrom(2048)
    except socket.timeout:
        continue

    receive_time = time.time()

    # 🔹 Chwilowe fs
    if last_time is not None:
        dt = receive_time - last_time
        if dt > 0:
            inst_fs = 1.0 / dt
            print(f"instant fs: {inst_fs:.1f} Hz")

    last_time = receive_time
    packet_counter += 1

    # 🔹 Dekodowanie JSON (bez crasha)
    try:
        packet = json.loads(data.decode())
    except json.JSONDecodeError:
        print("Błąd dekodowania JSON")

# ====== PODSUMOWANIE ======

total_time = time.time() - start_time

if total_time > 0:
    avg_fs = packet_counter / total_time
    print("\n===========================")
    print(f"Packets received: {packet_counter}")
    print(f"Total time: {total_time:.2f} s")
    print(f"REAL average fs ≈ {avg_fs:.2f} Hz")
    print("===========================")

sock.close()
