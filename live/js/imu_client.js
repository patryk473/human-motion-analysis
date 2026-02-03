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
      `AX: ${lastSample.ax}\nAY: ${lastSample.ay}\nAZ: ${lastSample.az}\n\n` +
      `GX: ${lastSample.gx}\nGY: ${lastSample.gy}\nGZ: ${lastSample.gz}\n\n` +
      `TS: ${lastSample.ts}`;

    //każda próbka trafia do sessionSamples
    sessionSamples.push({
      session_id: sessionId,
      sample_idx: sessionSamples.length,
      dt: dt,
      ax: lastSample.ax,
      ay: lastSample.ay,
      az: lastSample.az,
      gx: lastSample.gx,
      gy: lastSample.gy,
      gz: lastSample.gz,
      ts: currentTs
    });

  } catch (e) {
    document.getElementById("out").textContent = "Błąd połączenia";
    console.error("FETCH ERROR:", e);
  }

  timer = setTimeout(fetchIMU, REFRESH_MS);
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
    <td>${lastSample.ax}</td>
    <td>${lastSample.ay}</td>
    <td>${lastSample.az}</td>
    <td>${lastSample.gx}</td>
    <td>${lastSample.gy}</td>
    <td>${lastSample.gz}</td>
    <td>${lastSample.ts}</td>
    <td>
      <button onclick="deleteRow(this)">Usuń</button>
    </td>
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