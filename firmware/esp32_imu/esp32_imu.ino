#include <WiFi.h>
#include <WebServer.h>
#include "imu_sensor.h"
#include "api_handlers.h"

const char* ssid = "SPEED-NET-312019";
const char* password = "BB312019LAC6B1";

WebServer server(80);

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
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());

  // --- IMU ---
  imuInit();

  // --- HTTP API ---
  setupApi(server);
  server.begin();

  Serial.println("HTTP API uruchomione");
}

void loop() {
  server.handleClient();
}