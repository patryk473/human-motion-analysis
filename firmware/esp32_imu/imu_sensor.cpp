#include "imu_sensor.h"
#include <Wire.h>

static Adafruit_LSM6DS3TRC imu;

void imuInit() {
  Wire.begin(21, 22);

  if (!imu.begin_I2C(0x6A)) {
    Serial.println("❌ IMU nie wykryte");
    while (1);
  }

  imu.setAccelRange(LSM6DS_ACCEL_RANGE_4_G);
  imu.setGyroRange(LSM6DS_GYRO_RANGE_500_DPS);

  Serial.println("✅ IMU gotowe");
}

void imuRead(float &ax, float &ay, float &az,
             float &gx, float &gy, float &gz) {

  sensors_event_t a, g, t;
  imu.getEvent(&a, &g, &t);

  ax = a.acceleration.x;
  ay = a.acceleration.y;
  az = a.acceleration.z;

  gx = g.gyro.x;
  gy = g.gyro.y;
  gz = g.gyro.z;
}