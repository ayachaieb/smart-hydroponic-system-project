#include <SPI.h>
#include <Ethernet.h>
#include <PubSubClient.h>
#include <Wire.h>
#include <U8g2lib.h>
#include "Adafruit_CCS811.h"
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>
#include <Adafruit_GFX.h>
#include "Adafruit_SHT31.h"
#include "DFRobot_PH.h"
#include "DFRobot_EC10.h"
#include <EEPROM.h>
#include <ArduinoJson.h>
#include "MAX6675.h"
#include <avr/wdt.h>

// Pin Definitions
#define PH_PIN A0
#define EC_PIN A1
#define TRIG_PIN 19
#define ECHO_PIN 18
#define PUMP_PH_PIN 17
#define PUMP_A_PIN 16
#define PUMP_B_PIN 15
#define PUMP_WP_PIN 14

// Networking and MQTT Setup
byte mac[] = { 0xDE, 0xED, 0xBA, 0xFE, 0xFE, 0xED };
IPAddress server(10, 100, 50, 1);
EthernetClient ethClient;
PubSubClient client(server, 1883, callback, ethClient);

// Sensor Objects
Adafruit_CCS811 ccs;
MAX6675 thermoCouple(5, 4, 6);
Adafruit_SHT31 sht31 = Adafruit_SHT31();
DFRobot_PH PH;
DFRobot_EC10 EC;

// Global Variables
float voltage, ecValue, phValue, temperature = 25;
int buttonState = 0;
long lastActivationA, lastActivationB, lastActivationPH, lastActivationWaterPump;
long timerA, timerB, timerPH, timerWP = 20000;
long period = 30000;
String payloadPh, payloadWater, payloadTemp, payloadEc, payloadHumidity, payloadWaterTemp, payloadAirQuality;
float ph = 7, ec = 0, waterTemp = 0, humidity = 0, airTemp = 0, tvoc = 0, co2Value = 0;
long tCalib = millis(), tCalibEC = millis();

// Setup Function
void setup() {
  Serial.begin(9600);
  
  // Initialize Ethernet
  if (Ethernet.begin(mac) == 0) {
    Serial.println("Failed to configure Ethernet using DHCP");
  } else {
    Serial.print(F("IP Address assigned: "));
    Serial.println(Ethernet.localIP());
  }

  // Connect to MQTT
  if (reconnect()) {
    Serial.println("Connected to MQTT server");
    client.publish("room1/connected", "connected");
  }

  // Initialize Sensors
  initializeSensors();

  // Setup Pump Pins
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT_PULLUP);
  pinMode(PUMP_A_PIN, OUTPUT);
  pinMode(PUMP_B_PIN, OUTPUT);
  pinMode(PUMP_PH_PIN, OUTPUT);
  pinMode(PUMP_WP_PIN, OUTPUT);
  
  // Set initial pump state
  digitalWrite(PUMP_A_PIN, HIGH);
  digitalWrite(PUMP_B_PIN, HIGH);
  digitalWrite(PUMP_WP_PIN, HIGH);
  digitalWrite(PUMP_PH_PIN, HIGH);
}

// Loop Function
void loop() {
  client.loop();
  
  // Calibration Process
  handleCalibration();

  // Sensor Reading and Publishing
  if (millis() - lastActivationA > 20000) {
    readAndPublishSensors();
    lastActivationA = millis();
  }
  
  // Handle Pump Control
  handlePumpControl();
  
  // Send Keep-alive message
  client.publish("room1", "stay_active");
  
  // Water Level Measurement
  measureWaterLevel();
}

// Initialize Sensors
void initializeSensors() {
  if (!u8g2.begin()) {
    Serial.println(F("u8g2 initialization failed"));
  }
  if (!ccs.begin(0x5A)) {
    Serial.println("Failed to start CO2 sensor");
  }
  if (!sht31.begin(0x44)) {
    Serial.println("Failed to start SHT31 sensor");
  }
  PH.begin();
  EC.begin();
  SPI.begin();
  thermoCouple.begin();
  thermoCouple.setSPIspeed(4000000);
}

// Reconnect to MQTT Server
boolean reconnect() {
  while (!client.connected()) {
    if (client.connect("arduinoClient2", "room1/disconnect", 0, 0, "room1_disconnected")) {
      client.setKeepAlive(120000);
      client.subscribe("room1/ph/command");
      client.subscribe("room1/ec/command");
      client.subscribe("room1/waterLevel/command");
      client.subscribe("room1/ph/calib");
      client.subscribe("room1/ec/calib");
      return true;
    }
    Serial.println("Reconnection failed, retrying...");
    delay(5000);
  }
  return false;
}

// Handle Calibration Process
void handleCalibration() {
  if (calibration_status == 1) {
    calibratePH();
  }
  if (calibration_status_EC == 1) {
    calibrateEC();
  }
}

// Calibrate pH Sensor
void calibratePH() {
  PH.calibration(voltage, temperature, "enterph");
  delay(20000);
  PH.calibration(voltage, temperature, "calph");
  delay(20000);
  client.publish("room1/ph/calib_values", "calibration started");
  client.publish("room1/ph/calib/done", String(readPH(temperature)).c_str());
  calibration_status = 0;
}

// Calibrate EC Sensor
void calibrateEC() {
  EC.calibration(voltage, temperature, "enterec");
  delay(20000);
  EC.calibration(voltage, temperature, "calec");
  delay(20000);
  client.publish("room1/ec/calib_values", "calibration started");
  client.publish("room1/ec/calib/done", String(readec(temperature)).c_str());
  calibration_status_EC = 0;
}

// Read and Publish Sensor Data
void readAndPublishSensors() {
  humidity = readHumidity();
  airTemp = readTemperature();
  ph = readPH(airTemp);
  waterTemp = readWaterTemperature();
  co2Value = readAirQuality();
  tvoc = readTVOC();
  ec = readec(airTemp);

  publishSensorData("room1/ph/sensor", ph, payloadPh);
  publishSensorData("room1/waterLevel/sensor", distance, payloadWater);
  publishSensorData("room1/ec/sensor", ec, payloadEc);
  publishSensorData("room1/humidity/sensor", humidity, payloadHumidity);
  publishSensorData("room1/temperature/sensor", airTemp, payloadTemp);
  publishSensorData("room1/water_temp/sensor", waterTemp, payloadWaterTemp);
  publishSensorData("room1/air_quality/sensor", co2Value, payloadAirQuality);
}

// Publish Sensor Data to MQTT
void publishSensorData(const char* topic, float value, String &payload) {
  JsonDocument doc;
  doc["topic"] = topic;
  doc["Last_measure"] = value;
  serializeJson(doc, payload);
  client.publish(topic, payload.c_str());
}

// Read pH Value
float readPH(int temp) {
  voltage = analogRead(PH_PIN) / 1024.0 * 5000;
  phValue = PH.readPH(voltage, temp);
  return phValue;
}

// Read EC Value
float readec(int temp) {
  voltage = analogRead(EC_PIN) / 1024.0 * 5000;
  ecValue = EC.readEC(voltage, temp);
  return ecValue;
}

// Read Water Temperature
float readWaterTemperature() {
  float temp = thermoCouple.getTemperature() + waterTempOffset;
  return temp;
}

// Read Air Quality (CO2)
float readAirQuality() {
  if (ccs.available() && !ccs.readData()) {
    return ccs.geteCO2();
  }
  return -1;
}

// Read TVOC
float readTVOC() {
  return ccs.getTVOC();
}

// Read Humidity
float readHumidity() {
  return sht31.readHumidity();
}

// Read Air Temperature
float readTemperature() {
  return sht31.readTemperature() + airTempOffset;
}

// Measure Water Level
void measureWaterLevel() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(20);
  digitalWrite(TRIG_PIN, LOW);
  
  distance = pulseIn(ECHO_PIN, HIGH, 26000) / 58.0;
}

// Handle Pump Control
void handlePumpControl() {
  if ((millis() - lastActivationA) > timerA) {
    digitalWrite(PUMP_A_PIN, HIGH);
    lastActivationA = millis
