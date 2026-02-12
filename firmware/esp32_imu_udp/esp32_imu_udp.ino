#include <WiFi.h>
#include <WiFiUdp.h>
#include "imu_sensor_udp.h"

const char* ssid = "SPEED-NET-312019";
const char* password = "BB312019LAC6B1";

// 🔥 IP KOMPUTERA (Python)
IPAddress remoteIP(192,168,233,195);   // ← ZMIENISZ NA SWOJE
const unsigned int remotePort = 5005;

WiFiUDP udp;

unsigned long lastSend = 0;
const unsigned long intervalMs = 10;   // 100 Hz

void setup() {
  Serial.begin(115200);
  delay(1000);

  // --- WiFi ---
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  Serial.print("Laczenie z WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nPolaczono!");
  Serial.print("IP ESP32: ");
  Serial.println(WiFi.localIP());

  // --- IMU ---
  imuInit();

  udp.begin(1234);  // lokalny port (dowolny)

  Serial.println("UDP streaming uruchomione (100 Hz)");
}

void loop() {

  unsigned long now = millis();

  if (now - lastSend >= intervalMs) {
    lastSend = now;

    float ax0, ay0, az0, gx0, gy0, gz0;
    float ax1, ay1, az1, gx1, gy1, gz1;

    imuRead(0, ax0, ay0, az0, gx0, gy0, gz0);
    imuRead(1, ax1, ay1, az1, gx1, gy1, gz1);

    // 🔥 Minimalny JSON (2 IMU)
    String json = "{";

    json += "\"imu0\":{";
    json += "\"ax\":" + String(ax0,3) + ",";
    json += "\"ay\":" + String(ay0,3) + ",";
    json += "\"az\":" + String(az0,3) + ",";
    json += "\"gx\":" + String(gx0,3) + ",";
    json += "\"gy\":" + String(gy0,3) + ",";
    json += "\"gz\":" + String(gz0,3);
    json += "},";

    json += "\"imu1\":{";
    json += "\"ax\":" + String(ax1,3) + ",";
    json += "\"ay\":" + String(ay1,3) + ",";
    json += "\"az\":" + String(az1,3) + ",";
    json += "\"gx\":" + String(gx1,3) + ",";
    json += "\"gy\":" + String(gy1,3) + ",";
    json += "\"gz\":" + String(gz1,3);
    json += "},";

    json += "\"ts\":" + String(now);
    json += "}";

    udp.beginPacket(remoteIP, remotePort);
    udp.print(json);
    udp.endPacket();
  }
}
