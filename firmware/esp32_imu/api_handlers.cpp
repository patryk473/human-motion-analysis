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
    float ax0, ay0, az0, gx0, gy0, gz0;
    float ax1, ay1, az1, gx1, gy1, gz1;

    imuRead(0, ax0, ay0, az0, gx0, gy0, gz0);
    imuRead(1, ax1, ay1, az1, gx1, gy1, gz1);

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