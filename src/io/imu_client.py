# Jak to uruchomić?
# w bashu
"""
python src/io/imu_client.py

cd live
python -m http.server 8000
"""


from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from pathlib import Path
from datetime import datetime
import csv

app = Flask(__name__) #Działający lokalnie serwer http
CORS(app)

# Ścieżka bazowa projektu
BASE_DIR = Path(__file__).resolve().parents[2]

# Katalog na wyniki
OUT_DIR = BASE_DIR / "data" / "result"
OUT_DIR.mkdir(parents=True, exist_ok=True)

@app.route("/save_csv", methods=["OPTIONS"])
def save_csv_options():
    response = make_response()
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response, 204

@app.route("/save_csv", methods=["POST"])
def save_csv():
    payload = request.json    #Załadowanie danych do słownika Python
    samples = payload.get("samples", [])    #Pobranie listy próbek
    if not samples:
        return jsonify({"status": "error", "msg": "Brak próbek"}), 400
    
    # Znacznik czasu = unikalna nazwa sesji
    # Format czytelny + sortowalny
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Finalna ścieżka pliku CSV
    filename = OUT_DIR / f"imu_session_{timestamp}.csv"

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # Nagłówek CSV, Kolejność = kolejność sygnałów IMU
        writer.writerow([
            "session_id",
            "sample_idx",
            "dt",

            "imu0_ax", "imu0_ay", "imu0_az",
            "imu0_gx", "imu0_gy", "imu0_gz",

            "imu1_ax", "imu1_ay", "imu1_az",
            "imu1_gx", "imu1_gy", "imu1_gz",

            "ts"
        ])

        # Iterujemy po próbkach
        for s in samples:
            writer.writerow([
                s.get("session_id"),
                s.get("sample_idx"),
                s.get("dt"),

                s.get("imu0_ax"), s.get("imu0_ay"), s.get("imu0_az"),
                s.get("imu0_gx"), s.get("imu0_gy"), s.get("imu0_gz"),

                s.get("imu1_ax"), s.get("imu1_ay"), s.get("imu1_az"),
                s.get("imu1_gx"), s.get("imu1_gy"), s.get("imu1_gz"),

                s.get("ts")
            ])

    # Odpowiedź do serwera że dane zapisane - informacja diagnostyczna
    return jsonify({
        "status": "ok",
        "samples": len(samples)
    }), 200

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )