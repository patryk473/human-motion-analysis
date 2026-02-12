import socket
import json
import time

class IMUUDPReceiver:
    def __init__(self, host="0.0.0.0", port=5005):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((host, port))
        self.last_timestamp = None

    def receive(self):
        data, addr = self.sock.recvfrom(1024)
        packet = json.loads(data.decode())

        now = time.time()
        if self.last_timestamp:
            dt = now - self.last_timestamp
            print(f"fs ~ {1/dt:.1f} Hz")

        self.last_timestamp = now
        return packet
