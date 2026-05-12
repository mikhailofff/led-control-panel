import tkinter as tk
from tkinter import ttk
import json
import paho.mqtt.client as mqtt

MQTT_BROKER = "192.168.213.113"
MQTT_PORT = 1883
MQTT_TOPIC = "led/command"

try:
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
except AttributeError:
    client = mqtt.Client()

client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

current_direction = "none"

def send_mqtt(data):
    payload = json.dumps(data)
    client.publish(MQTT_TOPIC, payload)
    print(f"Отправлено: {payload}")

def toggle_led(pin, state):
    send_mqtt({"pin": pin, "action": "on" if state else "off"})

def send_speed_update(val):
    delay = int(float(val))
    lbl_current_speed.config(text=f"{delay} мс")

    send_mqtt({"action": "animation", "direction": "speed_only", "delay_ms": delay})

def start_animation(direction):
    global current_direction
    current_direction = direction
    lbl_status.config(text=f"Статус: Анимация [{direction.upper()}]", foreground="green")

    delay = int(speed_scale.get())
    send_mqtt({"action": "animation", "direction": "speed_only", "delay_ms": delay})
    root.after(20, lambda: send_mqtt({"action": "animation", "direction": direction, "delay_ms": delay}))

def stop_all():
    global current_direction
    current_direction = "none"
    lbl_status.config(text="Статус: Остановлено", foreground="red")
    send_mqtt({"action": "stop"})

root = tk.Tk()
root.title("Управление светодиодами (Задание 2)")
root.geometry("600x640")
root.resizable(False, False)

style = ttk.Style()
style.theme_use('clam')

lbl_status = ttk.Label(root, text="Статус: Готов к работе", font=("Arial", 10, "bold"), padding=10)
lbl_status.pack()

frame_manual = ttk.LabelFrame(root, text=" Ручное управление пинами ", padding=15)
frame_manual.pack(fill="x", padx=15, pady=5)

pins = [3, 5, 6, 9, 2]
for pin in pins:
    pin_frame = ttk.Frame(frame_manual)
    pin_frame.pack(fill="x", pady=4)

    lbl = ttk.Label(pin_frame, text=f"Пин Arduino {pin}: ", width=15)
    lbl.pack(side="left")

    btn_on = ttk.Button(pin_frame, text="Вкл", width=8, command=lambda p=pin: toggle_led(p, True))
    btn_on.pack(side="left", padx=2)

    btn_off = ttk.Button(pin_frame, text="Выкл", width=8, command=lambda p=pin: toggle_led(p, False))
    btn_off.pack(side="left", padx=2)

frame_anim = ttk.LabelFrame(root, text=" Бегущие огни ", padding=15)
frame_anim.pack(fill="x", padx=15, pady=5)

btn_forward = ttk.Button(frame_anim, text="◀ Вперед", command=lambda: start_animation("forward"))
btn_forward.pack(side="left", expand=True, padx=5)

btn_backward = ttk.Button(frame_anim, text="Назад ▶", command=lambda: start_animation("backward"))
btn_backward.pack(side="left", expand=True, padx=5)

frame_speed = ttk.LabelFrame(root, text=" Настройка задержки (скорости) ", padding=15)
frame_speed.pack(fill="x", padx=15, pady=5)

speed_scale = ttk.Scale(frame_speed, from_=50, to=500, value=200, orient="horizontal", command=send_speed_update)
speed_scale.pack(side="left", fill="x", expand=True, padx=5)

lbl_current_speed = ttk.Label(frame_speed, text="200 мс", width=8)
lbl_current_speed.pack(side="right", padx=5)

btn_stop = tk.Button(root, text="ОСТАНОВИТЬ ВСЁ", bg="#d9534f", fg="white",
                     font=("Arial", 12, "bold"), activebackground="#c9302c", command=stop_all)
btn_stop.pack(fill="x", padx=15, pady=15, ipady=8)

try:
    root.mainloop()
finally:
    client.loop_stop()
    client.disconnect()
