#include <OneWire.h>
#include <DallasTemperature.h>

#define ONE_WIRE_BUS 9
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

void setup() {
  Serial.begin(9600);
  while (!Serial) ; // Wait for USB enumeration
  sensors.begin();
}

void loop() {
  sensors.requestTemperatures();
  float tempC_1 = sensors.getTempCByIndex(0);
  float tempC_2 = sensors.getTempCByIndex(1);

  Serial.print("MAGIC_CT_SENSOR1,");
  Serial.println(tempC_1);

  Serial.print("MAGIC_CT_SENSOR2,");
  Serial.println(tempC_2);

  delay(1000);
}
