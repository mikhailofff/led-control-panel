# MQTT-SPI LED Control System

A distributed remote control system to manage LEDs on an Arduino mezzanine board via a communication chain: **PC (GUI) → MQTT → Lichee RV Dock → SPI → Arduino**.

## What it does
This project allows you to control hardware LEDs connected to an Arduino Uno from a PC graphical interface. It demonstrates how to bridge high-level network protocols (MQTT) with low-level hardware interfaces (SPI/GPIO) in an embedded environment.

## Key Features
- Individual LED toggling (Pins 3, 5, 6, 9, 2).
- Animated "running light" with adjustable speed.
- Real-time command synchronization using JSON over MQTT.

## How to run

### 1. Arduino
Flash `sketch.ino` to your **Arduino Uno**. It will act as an SPI Slave.

### 2. Lichee RV Dock (Gateway)
Ensure an MQTT broker (like Mosquitto) is running. Run the bridge script:
```bash
python3 mqtt_to_spi.py
```
*Requires: `spidev`, `paho-mqtt`.*

### 3. PC (Controller)
Launch the GUI application on your computer:
```bash
python3 gui_control.py
```
*Requires: `tkinter` and `paho-mqtt`.*

---

## Tech Stack
- **Python**: GUI (PC) and MQTT/SPI Bridge (Lichee).
- **C++/C**: Arduino Firmware.
- **Protocols**: MQTT, SPI.

