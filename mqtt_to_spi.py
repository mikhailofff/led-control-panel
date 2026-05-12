import spidev
import json
import time
import paho.mqtt.client as mqtt

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 500000
spi.mode = 0

def send_spi(byte_val):
    spi.xfer2([byte_val])
    print(f"Отправлен байт в SPI: {hex(byte_val)}")

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode('utf-8'))
        print(f"Получен JSON: {payload}")

        action = payload.get("action")

        if action == "stop":
            send_spi(0x00)
        elif action in ["on", "off"]:
            pin = payload.get("pin")
            state = 1 if action == "on" else 0

            mapping = {
                2: (0x09, 0x0A),
                3: (0x01, 0x02),
                5: (0x03, 0x04),
                6: (0x05, 0x06),
                9: (0x07, 0x08)
            }
            if pin in mapping:
                send_spi(mapping[pin][0] if state else mapping[pin][1])

        elif action == "animation":
            direction = payload.get("direction")
            delay_ms = payload.get("delay_ms", 150)

            cmd_delay = max(5, min(50, int(delay_ms / 10)))
            send_spi(cmd_delay)
            time.sleep(0.01)

            if direction == "forward":
                send_spi(0x11)
            elif direction == "backward":
                send_spi(0x12)

    except Exception as e:
        print(f"Ошибка обработки: {e}")

client = mqtt.Client()
client.on_message = on_message

client.connect("127.0.0.1", 1883, 60)
client.subscribe("led/command")

print("Шлюз MQTT-SPI запущен и ожидает команд в топике led/command...")
try:
    client.loop_forever()
finally:
    spi.close()
