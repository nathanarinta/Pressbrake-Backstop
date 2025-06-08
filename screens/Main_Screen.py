# screens/main_screen.py
import tkinter as tk
from tkinter import PhotoImage
from pathlib import Path
import json
import time

# GPIO setup for Raspberry Pi 5 or test mode
try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    STEP_PIN = 20  # adjust to your wiring
    DIR_PIN = 21   # adjust to your wiring
    GPIO.setup(STEP_PIN, GPIO.OUT)
    GPIO.setup(DIR_PIN, GPIO.OUT)
    ON_PI = True
    print(f"GPIO initialized: STEP_PIN={STEP_PIN}, DIR_PIN={DIR_PIN}")
except ImportError:
    ON_PI = False
    print("RPi.GPIO not available; running in test mode")


def build_main_screen(root, switch_to):
    frame = tk.Frame(root, bg="#FFFFFF")
    ASSETS_PATH = Path(r"C:/Users/arint/OneDrive/Desktop/Press Brake GUI/assets/main_screen/assets/frame0")
    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / path

    canvas = tk.Canvas(
        frame,
        bg="#FFFFFF",
        height=720,
        width=1280,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0)

    try:
        # Load calibration
        try:
            with open("settings.json", "r") as f:
                cfg = json.load(f)
            lead = float(cfg.get("lead", 0.0))
            steps_per_rev = int(cfg.get("steps_per_rev", 1))
            micro_steps = int(cfg.get("micro_steps", 1))
            in_per_microstep = lead / (steps_per_rev * micro_steps)
        except Exception as e:
            print("Error loading settings.json:", e)
            in_per_microstep = 1.0

        # State tracking
        current_position = [0.0]
        active_button_index = [None]

        # UI Setup
        bg_img = PhotoImage(file=relative_to_assets("image_1.png"))
        canvas.create_image(640, 360, image=bg_img)
        frame.bg_img = bg_img

        canvas.create_text(151, 202, anchor="nw", text="Custom", fill="#000000",
                            font=("IBMPlexMono Regular", 50 * -1))
        canvas.create_text(130, 15, anchor="nw", text="Current Location", fill="#000000",
                            font=("IBMPlexMono Regular", 64 * -1))

        image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
        canvas.create_image(943, 211, image=image_2)
        frame.image_2 = image_2

        # Entry for current position
        entry_img_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
        canvas.create_image(470, 235, image=entry_img_1)
        entry_1 = tk.Entry(frame, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
        entry_1.place(x=370, y=205, width=200, height=58)
        entry_1.insert(0, f"{current_position[0]:.3f}")
        frame.entry_img_1 = entry_img_1

        # Entry for optional manual input
        entry_img_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
        canvas.create_image(330.5, 125, image=entry_img_2)
        entry_2 = tk.Entry(frame, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
        entry_2.place(x=124, y=95, width=413, height=58)
        frame.entry_img_2 = entry_img_2

        # Button factory with toggle and hover
        def create_button(imgp, hovp, x, y, w, h, cmd=None, toggle_idx=None):
            img = PhotoImage(file=relative_to_assets(imgp))
            hov = PhotoImage(file=relative_to_assets(hovp))
            btn = tk.Button(frame, image=img, borderwidth=0, highlightthickness=0, relief="flat")

            def on_click():
                if toggle_idx is not None:
                    if active_button_index[0] == toggle_idx:
                        active_button_index[0] = None
                    else:
                        active_button_index[0] = toggle_idx
                    update_toggle_buttons()
                if cmd:
                    cmd()

            def on_enter(e):
                if active_button_index[0] != toggle_idx:
                    btn.config(image=hov)

            def on_leave(e):
                if active_button_index[0] != toggle_idx:
                    btn.config(image=img)

            btn.config(command=on_click)
            btn.place(x=x, y=y, width=w, height=h)
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
            frame.imgs.extend([img, hov])
            return btn, img, hov

        toggle_buttons = []
        def update_toggle_buttons():
            for i, (btn, img, hov) in enumerate(toggle_buttons):
                btn.config(image=(hov if active_button_index[0] == i else img))

        # Now that helper is defined, use it below
        # Home/Zero helpers
        def zero_home():
            current_position[0] = 0.0
            entry_2.delete(0, tk.END)
            entry_2.insert(0, f"{current_position[0]:.3f}")
            print("Zero pressed: home set to current position")

        def go_home():
            delta = -current_position[0]
            direction = "forward" if delta > 0 else "backward"
            move_by = abs(delta)
            steps_needed = int(move_by / in_per_microstep)
            print(f"--> Home: DIR={direction}, STEPS={steps_needed}")
            if ON_PI:
                GPIO.output(DIR_PIN, GPIO.HIGH if direction == "forward" else GPIO.LOW)
                for _ in range(steps_needed):
                    GPIO.output(STEP_PIN, GPIO.HIGH)
                    time.sleep(0.001)
                    GPIO.output(STEP_PIN, GPIO.LOW)
                    time.sleep(0.001)
            current_position[0] = 0.0
            entry_2.delete(0, tk.END)
            entry_2.insert(0, f"{current_position[0]:.3f}")

        # Movement helper
        def move_backstop(direction):
            if active_button_index[0] is not None:
                distances = [0.001, 0.1, 1, 0.01]
                move_by = distances[active_button_index[0]]
                steps_needed = int(move_by / in_per_microstep)
                print(f"--> DIR={direction}, STEPS={steps_needed}")
                if ON_PI:
                    GPIO.output(DIR_PIN, GPIO.HIGH if direction == "forward" else GPIO.LOW)
                    for _ in range(steps_needed):
                        GPIO.output(STEP_PIN, GPIO.HIGH)
                        time.sleep(0.001)
                        GPIO.output(STEP_PIN, GPIO.LOW)
                        time.sleep(0.001)
                if direction == "forward":
                    current_position[0] += move_by
                else:
                    current_position[0] -= move_by
                entry_2.delete(0, tk.END)
                entry_2.insert(0, f"{current_position[0]:.3f}")
            else:
                print("No distance selected")

        # Create distance toggle buttons
        frame.imgs = []
        toggle_buttons.append(create_button("button_1.png", "button_hover_1.png", 673, 397, 135, 60, toggle_idx=0))
        toggle_buttons.append(create_button("button_2.png", "button_hover_2.png", 943, 397, 135, 60, toggle_idx=1))
        toggle_buttons.append(create_button("button_3.png", "button_hover_3.png", 1078, 397, 135, 60, toggle_idx=2))
        toggle_buttons.append(create_button("button_4.png", "button_hover_4.png", 808, 397, 135, 60, toggle_idx=3))

        # Zero button (5)
        frame.imgs += create_button("button_5.png", "button_hover_5.png", 547, 95, 73, 60, cmd=zero_home)
        # Bend sequence nav
        frame.imgs += create_button("button_7.png", "button_hover_6.png", 215, 306, 300, 58, cmd=lambda: switch_to("bend_sequence_setup"))
                # Home button (mapped to go_home)
        frame.imgs += create_button(
            "button_8.png", "button_hover_7.png",
            215, 395, 300, 60,
            cmd=go_home
        )
        # Home button (9)
        frame.imgs += create_button("button_9.png", "button_hover_8.png", 608, 205, 150, 60, cmd=go_home)
        # Forward (10) & Back (11)
        frame.imgs += create_button("button_10.png", "button_hover_9.png", 868, 307, 150, 60, cmd=lambda: move_backstop("forward"))
        frame.imgs += create_button("button_11.png", "button_hover_10.png", 868, 57, 150, 60, cmd=lambda: move_backstop("backward"))

        # Settings nav (Exit)
        btn6 = PhotoImage(file=relative_to_assets("button_6.png"))
        b6 = tk.Button(frame, image=btn6, borderwidth=0, highlightthickness=0, relief="flat",
                       command=lambda: switch_to("settings"))
        b6.place(x=1220, y=660, width=60, height=60)
        frame.btn_img_6 = btn6

    except Exception as e:
        print(f"Error loading main screen: {e}")
    return frame
