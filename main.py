import tkinter as tk
from tkinter import ttk
import time
import random
import string
import pyautogui
import threading
alphabet_chars = string.ascii_letters

def stop_typing():
    root.destroy() # close the window 
    sys.exit(0)


def start_typing():
    text = text_box.get("1.0", tk.END).rstrip()
    try:
        rpm = int(rpm_entry.get())
    except ValueError:
        status_label.config(text="RPM must be a number")
        return

    random_enabled = random_var.get()

    delay = 60 / rpm

    # Run typing in a separate thread so GUI doesn't freeze
    threading.Thread(target=type_text, args=(
        text, delay, random_enabled), daemon=True).start()


def type_text(text, delay, random_enabled):
    status_label.config(
        text="Starting in 5 seconds… click into your target window")
    time.sleep(5)

    for char in text:
        status_label.config(text="Typing...")
        if char == " ":
            wrongChar = random.choice(alphabet_chars) + char
            pyautogui.write(wrongChar)
            jitter = random.uniform(-0.01, 0.01)
            time.sleep(max(0, delay + jitter))
            pyautogui.press('backspace')
            time.sleep(max(0, delay + jitter))
            pyautogui.press('backspace')

        pyautogui.write(char)
        print(char)
        if random_enabled:
            jitter = random.uniform(-0.02, 0.02)
            time.sleep(max(0, delay + jitter))
        else:
            time.sleep(delay)

    status_label.config(text="Done typing")


# GUI setup
root = tk.Tk()
root.title("Auto Typer")

frame = ttk.Frame(root, padding=10)
frame.grid()

ttk.Label(frame, text="Text to type:").grid(row=0, column=0, sticky="w")
text_box = tk.Text(frame, width=50, height=10)
text_box.grid(row=1, column=0, columnspan=2, pady=5)

ttk.Label(frame, text="Characters per minute (RPM):").grid(
    row=2, column=0, sticky="w")
rpm_entry = ttk.Entry(frame)
rpm_entry.grid(row=2, column=1, sticky="e")

random_var = tk.BooleanVar()
random_check = ttk.Checkbutton(
    frame, text="Enable random delays and text", variable=random_var)
random_check.grid(row=3, column=0, columnspan=2, pady=5)

start_button = ttk.Button(frame, text="Start Typing", command=start_typing)
start_button.grid(row=4, column=0, columnspan=2, pady=10)

stop_button = ttk.Button(frame, text="Stop Typing", command=stop_typing)
stop_button.grid(row=8, column = 0) columnspan=2, pady=10)

status_label = ttk.Label(frame, text="")
status_label.grid(row=5, column=0, columnspan=2)

root.mainloop()
