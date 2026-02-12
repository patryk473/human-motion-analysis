#include "imu_sensor_udp.h"
#include <Wire.h>

static Adafruit_LSM6DS3TRC imu0; // np. udo
static Adafruit_LSM6DS3TRC imu1; // np. lydka

void imuInit() {
  Wire.begin(21, 22);

  bool ok0 = imu0.begin_I2C(0x6A);
  bool ok1 = imu1.begin_I2C(0x6B);

  if (!ok0 || !ok1) {
    Serial.println("❌ Nie wykryto obu IMU");
    Serial.print("IMU0: "); Serial.println(ok0 ? "OK" : "BRAK");
    Serial.print("IMU1: "); Serial.println(ok1 ? "OK" : "BRAK");
    while (1);
  }

  imu0.setAccelRange(LSM6DS_ACCEL_RANGE_4_G);
  imu0.setGyroRange(LSM6DS_GYRO_RANGE_500_DPS);

  imu1.setAccelRange(LSM6DS_ACCEL_RANGE_4_G);
  imu1.setGyroRange(LSM6DS_GYRO_RANGE_500_DPS);

  Serial.println("✅ Oba IMU gotowe");
}

bool imuRead(
  int id,
  float &ax, float &ay, float &az,
  float &gx, float &gy, float &gz
) {
  sensors_event_t a, g, t;

  if (id == 0) {
    imu0.getEvent(&a, &g, &t);
  } else if (id == 1) {
    imu1.getEvent(&a, &g, &t);
  } else {
    return false;
  }

  ax = a.acceleration.x;
  ay = a.acceleration.y;
  az = a.acceleration.z;

  gx = g.gyro.x;
  gy = g.gyro.y;
  gz = g.gyro.z;

  return true;
}