import tkinter as tk
from tkinter import ttk
import threading
import time
import random
import string
import pyautogui

class AutoTyperApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Auto Typer")
        self.root.geometry("600x600")

        self.typing_thread = None
        self.stop_flag = False

        self.build_gui()

    # ---------------- GUI ---------------- #

    def build_gui(self):
        main = ttk.Frame(self.root, padding=15)
        main.pack(fill="both", expand=True)

        # Text input
        ttk.Label(main, text="Text to Type:").pack(anchor="w")
        self.text_box = tk.Text(main, height=10)
        self.text_box.pack(fill="x", pady=5)

        # WPM
        settings_frame = ttk.LabelFrame(main, text="Typing Settings", padding=10)
        settings_frame.pack(fill="x", pady=10)

        ttk.Label(settings_frame, text="Words Per Minute (WPM):").grid(row=0, column=0, sticky="w")
        self.wpm_entry = ttk.Entry(settings_frame)
        self.wpm_entry.insert(0, "60")
        self.wpm_entry.grid(row=0, column=1)

        # Randomness strength
        ttk.Label(settings_frame, text="Randomness Strength:").grid(row=1, column=0, sticky="w")
        self.random_slider = ttk.Scale(settings_frame, from_=0, to=0.2, orient="horizontal")
        self.random_slider.set(0.05)
        self.random_slider.grid(row=1, column=1, sticky="ew")

        # Options
        self.jitter_var = tk.BooleanVar(value=True)
        self.pause_var = tk.BooleanVar(value=True)
        self.typo_var = tk.BooleanVar(value=True)

        ttk.Checkbutton(settings_frame, text="Enable Natural Jitter", variable=self.jitter_var)\
            .grid(row=2, column=0, columnspan=2, sticky="w")

        ttk.Checkbutton(settings_frame, text="Enable Thinking Pauses", variable=self.pause_var)\
            .grid(row=3, column=0, columnspan=2, sticky="w")

        ttk.Checkbutton(settings_frame, text="Enable Typos", variable=self.typo_var)\
            .grid(row=4, column=0, columnspan=2, sticky="w")

        # Countdown
        ttk.Label(settings_frame, text="Countdown Before Start (seconds):")\
            .grid(row=5, column=0, sticky="w")
        self.countdown_entry = ttk.Entry(settings_frame)
        self.countdown_entry.insert(0, "5")
        self.countdown_entry.grid(row=5, column=1)

        settings_frame.columnconfigure(1, weight=1)

        # Buttons
        button_frame = ttk.Frame(main)
        button_frame.pack(pady=10)

        self.start_button = ttk.Button(button_frame, text="Start Typing", command=self.start_typing)
        self.start_button.grid(row=0, column=0, padx=5)

        self.stop_button = ttk.Button(button_frame, text="Stop", command=self.stop_typing)
        self.stop_button.grid(row=0, column=1, padx=5)

        # Status
        self.status_label = ttk.Label(main, text="Idle")
        self.status_label.pack(pady=10)

    # ---------------- Control ---------------- #

    def start_typing(self):
        if self.typing_thread and self.typing_thread.is_alive():
            return

        text = self.text_box.get("1.0", tk.END).rstrip()
        if not text:
            self.update_status("Text box is empty.")
            return

        try:
            wpm = float(self.wpm_entry.get())
            if wpm <= 0:
                raise ValueError
        except ValueError:
            self.update_status("WPM must be a positive number.")
            return

        try:
            countdown = int(self.countdown_entry.get())
            if countdown < 0:
                raise ValueError
        except ValueError:
            self.update_status("Countdown must be 0 or higher.")
            return

        self.stop_flag = False
        self.start_button.config(state="disabled")

        delay = 60 / (wpm * 5)  # real WPM calculation

        self.typing_thread = threading.Thread(
            target=self.type_text,
            args=(text, delay, countdown),
            daemon=True
        )
        self.typing_thread.start()

    def stop_typing(self):
        self.stop_flag = True
        self.update_status("Stopping...")

    # ---------------- Typing Logic ---------------- #

    def type_text(self, text, base_delay, countdown):
        self.update_status(f"Starting in {countdown} seconds...")

        for i in range(countdown):
            if self.stop_flag:
                self.finish()
                return
            time.sleep(1)

        alphabet = string.ascii_letters

        self.update_status("Typing...")

        for char in text:
            if self.stop_flag:
                self.finish()
                return

            # Simulate typo
            if self.typo_var.get() and random.random() < 0.03 and char != " ":
                wrong = random.choice(alphabet)
                pyautogui.write(wrong)
                time.sleep(0.1)
                pyautogui.press("backspace")

            pyautogui.write(char)

            sleep_time = base_delay

            # Jitter
            if self.jitter_var.get():
                strength = self.random_slider.get()
                sleep_time += random.uniform(-strength, strength)

            # Thinking pause
            if self.pause_var.get():
                if random.random() < 0.03:
                    sleep_time += random.uniform(0.3, 0.8)

                if char in ".!?":
                    sleep_time += random.uniform(0.3, 0.6)

                if char in ",;:":
                    sleep_time += random.uniform(0.1, 0.3)

            time.sleep(max(0, sleep_time))

        self.finish()

    # ---------------- Helpers ---------------- #

    def update_status(self, text):
        self.root.after(0, lambda: self.status_label.config(text=text))

    def finish(self):
        self.update_status("Done.")
        self.root.after(0, lambda: self.start_button.config(state="normal"))


# ---------------- Run App ---------------- #

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoTyperApp(root)
    root.mainloop()
