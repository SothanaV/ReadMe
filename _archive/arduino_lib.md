# Wemos / ESP8266 Arduino Setup

> **Archived** — This document covers setup for the Wemos D1 Mini (ESP8266) board in the Arduino IDE.

## Board Manager URL

Add the following URL in Arduino IDE under **File > Preferences > Additional Boards Manager URLs**:

```text
http://arduino.esp8266.com/stable/package_esp8266com_index.json
```

Then install the **esp8266** board package via **Tools > Board > Boards Manager**.

## Required Libraries

Install the following libraries via **Tools > Manage Libraries** or download manually.

### Hardware Interface

| Library   | Purpose                        |
| --------- | ------------------------------ |
| MCP4725   | 12-bit DAC over I2C            |
| MCP3208   | 8-channel 12-bit ADC over SPI  |
| Wire      | I2C communication              |
| SPI       | SPI communication              |

### Connectivity

| Library              | Purpose                                    |
| -------------------- | ------------------------------------------ |
| ESP8266WiFi          | Core Wi-Fi library for ESP8266             |
| ESP8266WiFiMulti     | Connect to multiple Wi-Fi networks         |
| ESP8266HTTPClient    | HTTP client for making web requests        |

### Sensors

| Library             | Purpose                                          |
| ------------------- | ------------------------------------------------ |
| DHT sensor library  | Temperature and humidity sensor (DHT11/DHT22)    |

## References

- [ESP8266 Arduino Core Documentation](https://arduino-esp8266.readthedocs.io/)
- [Wemos D1 Mini Pinout](https://www.wemos.cc/en/latest/d1/d1_mini.html)
