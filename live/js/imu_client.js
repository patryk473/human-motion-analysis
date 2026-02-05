console.log("IMU CLIENT JS ZAŁADOWANY");
const ESP_IP = "http://192.168.233.26"; // <- IP ESP32
const PY_API = "http://localhost:5000"; // <- adres backendu Python
const REFRESH_MS = 100; // 100 ms = 10 Hz <- częstotliwość odświeżania

let running = false;
let timer = null;
let lastSample = null;
let sampleCount = 0; //ostatnia próbka (do podglądu)
let sessionSamples = []; //zapisane próbki między start i stop
let sessionId = null;     // unikalny ID sesji
let lastTs = null;       // timestamp poprzedniej próbki

// --- LIVE ---
async function fetchIMU() {
  if (!running) return;

  try {
    const res = await fetch(ESP_IP + "/data");
    lastSample = await res.json();

    const currentTs = lastSample.ts;

    // dt w sekundach
    let dt = 0.0;
    if (lastTs !== null) {
      dt = (currentTs - lastTs) / 1000.0;
    }
    lastTs = currentTs;

    //Last sample do podglądu Live
    document.getElementById("out").textContent =
    `IMU 0 (UDO)
    AX: ${lastSample.imu0.ax}
    AY: ${lastSample.imu0.ay}
    AZ: ${lastSample.imu0.az}
    GX: ${lastSample.imu0.gx}
    GY: ${lastSample.imu0.gy}
    GZ: ${lastSample.imu0.gz}

    IMU 1 (ŁYDKA)
    AX: ${lastSample.imu1.ax}
    AY: ${lastSample.imu1.ay}
    AZ: ${lastSample.imu1.az}
    GX: ${lastSample.imu1.gx}
    GY: ${lastSample.imu1.gy}
    GZ: ${lastSample.imu1.gz}

    TS: ${lastSample.ts}`;

    //każda próbka trafia do sessionSamples
    sessionSamples.push({
      session_id: sessionId,
      sample_idx: sessionSamples.length,
      dt: dt,

      imu0_ax: lastSample.imu0.ax,
      imu0_ay: lastSample.imu0.ay,
      imu0_az: lastSample.imu0.az,
      imu0_gx: lastSample.imu0.gx,
      imu0_gy: lastSample.imu0.gy,
      imu0_gz: lastSample.imu0.gz,

      imu1_ax: lastSample.imu1.ax,
      imu1_ay: lastSample.imu1.ay,
      imu1_az: lastSample.imu1.az,
      imu1_gx: lastSample.imu1.gx,
      imu1_gy: lastSample.imu1.gy,
      imu1_gz: lastSample.imu1.gz,

      ts: currentTs
    });

  } catch (e) {
    document.getElementById("out").textContent = "Błąd połączenia";
    console.error("FETCH ERROR:", e);
  }

  if (running) {
    timer = setTimeout(fetchIMU, REFRESH_MS);
  }
}

//start pomiaru i zerowanie sessionSamples
function start() {
  if (running) return;

  sessionSamples = [];
  lastTs = null;

  // session_id = timestamp startu sesji
  sessionId = new Date().toISOString()
    .replace(/[-:.TZ]/g, "")
    .slice(0, 14);

  running = true;
  fetchIMU();
}

//koniec pomiaru. Funkcja running przyjmuje stop i nie działa już fetch
function stop() {
  running = false;

  if (timer !== null) {
    clearTimeout(timer);
    timer = null;
  }

  if (timer) clearTimeout(timer);
  document.getElementById("out").textContent = "Zatrzymano";

  // Jeśli mamy dane – zapisujemy
  if (sessionSamples.length > 0) {
    sendSessionToPython();
  }
}

// --- ZAPIS PRÓBKI ---
function saveSample() {
  if (!lastSample) return;

  sampleCount++;

  const row = document.createElement("tr");
  row.innerHTML = `
  <td>${sampleCount}</td>

  <td>${lastSample.imu0.ax}</td>
  <td>${lastSample.imu0.ay}</td>
  <td>${lastSample.imu0.az}</td>
  <td>${lastSample.imu0.gx}</td>
  <td>${lastSample.imu0.gy}</td>
  <td>${lastSample.imu0.gz}</td>

  <td>${lastSample.imu1.ax}</td>
  <td>${lastSample.imu1.ay}</td>
  <td>${lastSample.imu1.az}</td>
  <td>${lastSample.imu1.gx}</td>
  <td>${lastSample.imu1.gy}</td>
  <td>${lastSample.imu1.gz}</td>

  <td>${lastSample.ts}</td>
  <td><button onclick="deleteRow(this)">Usuń</button></td>
  `;

  document.getElementById("samples").appendChild(row);
}

function deleteRow(button) {
  const row = button.parentNode.parentNode;
  row.remove();
}

//Wysyła całą sesję
function sendSessionToPython() {
  fetch(PY_API + "/save_csv", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      source: "imu",
      samples: sessionSamples
    })
  })
  .then(res => res.json())
  .then(data => {
    console.log("CSV zapisany:", data.file);
  })
  .catch(err => {
    console.error("Błąd zapisu CSV", err);
  });
}