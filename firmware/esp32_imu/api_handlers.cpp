#include "api_handlers.h"
#include "imu_sensor.h"

static int sampleRateHz = 50;
static bool streamingEnabled = false;

void setupApi(WebServer &server) {

  // GET /
  server.on("/", HTTP_GET, [&]() {
    server.send(200, "text/plain", "ESP32 HTTP dziala");
  });

  // GET /status
  server.on("/status", HTTP_GET, [&]() {
    String json = "{";
    json += "\"device\":\"ESP32\",";
    json += "\"wifi\":\"connected\",";
    json += "\"ip\":\"" + server.client().localIP().toString() + "\"";
    json += "}";

    server.send(200, "application/json", json);
  });

  // GET /data
  server.on("/data", HTTP_GET, [&]() {
    float ax, ay, az, gx, gy, gz;
    imuRead(ax, ay, az, gx, gy, gz);

    String json = "{";
    json += "\"ax\":" + String(ax, 3) + ",";
    json += "\"ay\":" + String(ay, 3) + ",";
    json += "\"az\":" + String(az, 3) + ",";
    json += "\"gx\":" + String(gx, 3) + ",";
    json += "\"gy\":" + String(gy, 3) + ",";
    json += "\"gz\":" + String(gz, 3) + ",";
    json += "\"ts\":" + String(millis());
    json += "}";

    server.sendHeader("Access-Control-Allow-Origin", "*");
    server.send(200, "application/json", json);
  });

  // GET /config
  server.on("/config", HTTP_GET, [&]() {
    String json = "{";
    json += "\"sampleRateHz\":" + String(sampleRateHz) + ",";
    json += "\"streaming\":" + String(streamingEnabled ? "true" : "false");
    json += "}";

    server.send(200, "application/json", json);
  });

  // POST /config
  server.on("/config", HTTP_POST, [&]() {
    if (server.hasArg("sampleRateHz")) {
      sampleRateHz = server.arg("sampleRateHz").toInt();
    }

    if (server.hasArg("streaming")) {
      streamingEnabled = (server.arg("streaming") == "true");
    }

    server.send(200, "application/json", "{\"status\":\"ok\"}");
  });
}