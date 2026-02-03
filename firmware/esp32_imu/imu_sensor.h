#pragma once
#include <Adafruit_LSM6DS3TRC.h>

void imuInit();
void imuRead(float &ax, float &ay, float &az,
             float &gx, float &gy, float &gz);