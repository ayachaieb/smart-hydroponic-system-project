# Smart Hydroponics System with MQTT Integration

This project involves a Smart Hydroponics System designed to monitor and control various parameters like pH levels, water temperature, EC (Electrical Conductivity), humidity, air quality (CO2 and TVOC), and water level. The system also includes automatic control of pumps for adding nutrients, pH adjustments, and water circulation. It uses MQTT for communication and real-time data publishing.

---

## Table of Contents

- [Overview](#overview)
- [photo](#photo)
- [Components](#components)
- [Mechanical Design](#Mechanical-Design)
- [PCB Enclosure Design](#PCB-Enclosure-Design)
- [System Architecture](#system-architecture)
- [Features](#features)
- [MQTT Topics](#mqtt-topics)
- [Wiring Diagram](#wiring-diagram)
- [Setup Instructions](#setup-instructions)
- [Libraries and Dependencies](#libraries-and-dependencies)
- [Code Explanation](#code-explanation)
- [Calibration](#calibration)
- [Troubleshooting](#troubleshooting)

---

## Overview

This Smart Hydroponics System monitors and controls critical factors for plant growth in a hydroponic environment. It features real-time monitoring of:

- **pH levels**
- **Electrical Conductivity (EC)**
- **Water temperature**
- **Humidity**
- **Air quality (CO2 and TVOC)**
- **Water level**

The system can adjust pH levels and EC by controlling pumps that add necessary chemicals to the hydroponic solution. The system also sends real-time data to a cloud server via MQTT for remote monitoring and control.

---
## photo
![alt text](https://ibb.co/5KvJCG7)

## Components

- **Microcontroller:** Arduino or compatible board (e.g., Arduino Uno or Mega)
- **Ethernet Shield:** For Ethernet connectivity
- **Sensors:**
  - **pH Sensor:** Measures the pH level of the solution
  - **EC Sensor:** Measures the electrical conductivity of the solution
  - **Temperature Sensor (MAX6675):** Measures water temperature
  - **Humidity and temperature Sensor (SHT31):** Measures air temperature and humidity
  - **Air Quality Sensor (CCS811):** Measures CO2 and TVOC levels
  - **Ultrasonic Sensor (HC-SR04):** Measures water level in the tank
- **Actuators:**
  - **Water Pumps:** For injecting water, nutrients, and pH adjustments
- **Other Modules:**
  - **Display (SSD1306 OLED):** For local display of system status
  - **Ethernet Shield:** For network communication using MQTT

---
## Mechanical Design
The mechanical design of the hydroponic system was created to support a scalable and efficient setup. The system consists of various components, including the frame, sensor mounts, and water pumps.
--The design incorporates modular parts that can be easily assembled.
--The sensors are mounted on adjustable arms to allow for easy calibration and maintenance.
--The water circulation and pH control systems are integrated into the base of the setup, ensuring effective nutrient distribution.
 Files are accessible at the "mechanic design of hydroponic system" folder.
 ---
## PCB Enclosure Design
The PCB enclosure is designed to house all the electronics securely, protecting them from external elements and ensuring efficient airflow for heat dissipation. The following files are provided for the PCB enclosure design:

PCB Enclosure Design Files are accessible at the "pcb_enclosure design" folder
---
## System Architecture

### High-level Design:
1. **Sensor Readings:**
   - Sensors continuously collect data (pH, EC, temperature, humidity, CO2, TVOC, and water level).
   - Data is processed and stored locally on the microcontroller.

2. **Control Logic:**
   - The microcontroller uses sensor readings to decide when to activate pumps (for pH adjustment, EC control, or water circulation).
   - The control logic is time-based and adjustable via MQTT commands.

3. **Data Transmission:**
   - Sensor data is transmitted to an MQTT broker (e.g., cloud or local server).
   - The system subscribes to commands via MQTT to control pumps or adjust parameters.

4. **User Interaction:**
   - The system can receive commands from a remote server via MQTT to adjust the operation of pumps or modify system behavior (e.g., calibrating sensors).

---

## Features

- **Real-time Monitoring:**
  - The system continuously monitors:
    - pH levels
    - EC (electrical conductivity)
    - Temperature (water and air)
    - Humidity
    - Air Quality (CO2 and TVOC)
    - Water level
- **Automatic Control:**
  - The system can adjust pH and EC levels by activating pumps.
  - It controls the water circulation pump based on water level readings.
- **Remote Control & Data Logging via MQTT:**
  - MQTT messages are published for each sensor's readings.
  - The system can subscribe to specific topics to control pumps or start/stop actions based on incoming MQTT messages.
- **Local Display:**
  - The system displays critical data (temperature, humidity, pH, etc.) on an OLED display for local monitoring.
- **commmunication whith the cloud via rasberry pi :**
- **calibration through cloud or mobile app:**
Sure! Here’s a more concise version with an overview of the **Dynamic IP Addressing (DHCP)** for Arduinos and **UUID Generation** for Raspberry Pi:

- **Dynamic IP Address Assignment (DHCP) for Arduino Devices**

Each Arduino in the system is assigned a **dynamic IP address** using **DHCP (Dynamic Host Configuration Protocol)**. This allows each Arduino to automatically request an IP address from the local network without manual configuration. As a result, Arduinos can seamlessly join the network and easily scale across multiple rooms in the hydroponic system, each receiving a unique IP upon connection.

### Key Points:
- **Dynamic IP assignment** ensures flexibility and scalability.
- Arduinos communicate with the Raspberry Pi via MQTT using their dynamically assigned IP addresses.
- Simplifies network management as the system expands.

- **UUID Generation on Raspberry Pi**

Each **Raspberry Pi** running the local MQTT broker generates a **unique UUID** upon startup. This UUID is used to uniquely identify the Raspberry Pi in the system, allowing for distinct identification of each room's MQTT broker and ensuring proper communication between devices. The UUID is incorporated into the **MQTT client ID**, making it easy to distinguish and manage data from each Raspberry Pi instance.

### Key Points:
- **Unique UUIDs** are generated for each Raspberry Pi to identify it across the system.
- The **UUID** is used in MQTT client identification for seamless communication.
- Each Raspberry Pi runs its own **local MQTT broker** that handles data from Arduinos and communicates with the central system.

## MQTT Topics

The system uses the MQTT protocol to communicate with an external server for monitoring and controlling the hydroponic system. Below are the main MQTT topics:

### Topics for Sensor Data:
- `room1/ph/sensor`: pH level
- `room1/ec/sensor`: EC (electrical conductivity) value
- `room1/temperature/sensor`: Water temperature
- `room1/humidity/sensor`: Humidity
- `room1/waterLevel/sensor`: Water level
- `room1/air_quality/sensor`: CO2 and TVOC levels

### Topics for Control Commands:
- `room1/ph/command`: Adjust the pH by controlling the pH pump
- `room1/ec/command`: Adjust EC levels using nutrient pumps
- `room1/waterLevel/command`: Control the water pump based on water level
- `room1/ph/calib`: start ph Calibration 
- `room1/ec/calib`: Calibration command for the EC sensor

---

## Wiring Diagram

The following components are connected to an Arduino using the following pins:

- **pH Sensor:** Connected to analog pin `A0`
- **EC Sensor:** Connected to analog pin `A1`
- **Ultrasonic Sensor (Water Level):**
  - Trigger (TRIG) pin to digital pin `19`
  - Echo (ECHO) pin to digital pin `18`
- **Temperature Sensor (MAX6675):**
  - Select (CS) pin to digital pin `5`
  - Data (DO) pin to digital pin `4`
  - Clock (CK) pin to digital pin `6`
- **Display (OLED SSD1306):** Connected to I2C pins (SDA, SCL)
- **Pumps:** Control pins for different pumps (`pumpA`, `pumpB`, `pumpPH`, `pumpwp`) are connected to digital pins `15`, `16`, `17`, `14`.

---

## Setup Instructions

### Hardware Setup:
1. **Connect the sensors** (pH, EC, SHT31, CCS811, MAX6675) to the Arduino following the pinout mentioned above.
2. **Connect the pumps** (pH pump, nutrient pumps, water pump) to their respective control pins.
3. **Connect the Ethernet shield** to the Arduino to enable network communication.
4. **Connect the OLED display** to the I2C bus for real-time data display.

### Software Setup:
1. **Install the Arduino IDE**: If you don’t have the Arduino IDE, download and install it from [here](https://www.arduino.cc/en/software).
2. **Install Required Libraries**: Ensure you have the following libraries installed:
   - `PubSubClient` for MQTT communication.
   - `Adafruit_SHT31` for the SHT31 humidity sensor.
   - `Adafruit_BME280` for environmental data.
   - `Adafruit_CCS811` for the air quality sensor.
   - `U8g2lib` for the OLED display.
   - `MAX6675` for the temperature sensor.
   - `DFRobot_PH` for the pH sensor.
   - `DFRobot_EC10` for the EC sensor.
3. **Upload the Code**: Open the Arduino IDE, select the correct board and port, and upload the code to the Arduino.

### MQTT Setup:
1. **Broker Setup**: You can use any MQTT broker like [Mosquitto](https://mosquitto.org/) or cloud-based brokers (e.g., AWS IoT, HiveMQ).
i used local broker at rasberry pi 
2. **Server Configuration**: Update the IP address of your MQTT broker in the Arduino code.


## Libraries and Dependencies

1. `Adafruit_SHT31`
2. `Adafruit_BME280`
3. `Adafruit_CCS811`
4. `U8g2lib`
5. `MAX6675`
6. `DFRobot_PH`
7. `DFRobot_EC10`
8. `PubSubClient` (for MQTT)

You can install these libraries using the Arduino Library Manager.



## Code Explanation

The code is divided into several main functions:

1. **`setup()`**: Initializes the sensors, pumps, Ethernet connection, and MQTT client.
2. **`loop()`**: Continuously reads sensor values, checks if any pump needs to be activated based on control logic, and sends sensor data via MQTT.
3. **`callback()`**: This function handles incoming MQTT messages for control commands like adjusting pH, EC, or water pumps.
4. **`reconnect()`**: Ensures that the device remains connected to the MQTT broker and subscribes to the relevant topics.
5. **Sensor Reading Functions**: Functions like `readPH()`, `readEC()`, `readtemp()`, etc., read the respective sensor values.


## Calibration

Calibration for both pH and EC sensors can be triggered by sending MQTT commands to `room1/ph/calib` or `room1/ec/calib`. or by mobile application  The system will start the calibration process for each sensor and publish the status.

## additional information
If you have any questions, need further assistance, or would like to contribute to the project, feel free to reach out! You can contact us through the following channels:

Contact Details:
mail: eya.chaieb@insat.ucar.tn
Linkedin: https://www.linkedin.com/in/eya-chaieb-80a455281/
