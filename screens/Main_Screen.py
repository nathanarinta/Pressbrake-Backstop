# screens/main_screen.py
import tkinter as tk
from tkinter import PhotoImage
from pathlib import Path
import json
import time

# Shared hardware pins
from hardware import STEP_PIN, DIR_PIN, ON_PI


def build_main_screen(root, switch_to):
    frame = tk.Frame(root, bg="#FFFFFF")

    # Hard-coded Pi asset folder
    ASSETS_PATH = Path("/home/nathanarinta/PressGUI/assets/main_screen/assets/frame0")

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
            lead            = float(cfg.get("lead",      0.0))
            steps_per_rev   = int(cfg.get("steps_per_rev",1))
            micro_steps     = int(cfg.get("micro_steps",  1))
            in_per_microstep = lead / (steps_per_rev * micro_steps)
        except Exception as e:
            print("Error loading settings.json:", e)
            in_per_microstep = 1.0

        # State tracking
        current_position  = [0.0]
        active_button_idx = [None]

        # UI Setup
        bg_img = PhotoImage(file=str(relative_to_assets("image_1.png")))
        canvas.create_image(640, 360, image=bg_img)
        frame.bg_img = bg_img

        canvas.create_text(
            151, 202, anchor="nw",
            text="Custom", fill="#000000",
            font=("IBMPlexMono Regular", -50)
        )
        canvas.create_text(
            130, 15, anchor="nw",
            text="Current Location", fill="#000000",
            font=("IBMPlexMono Regular", -64)
        )

        image_2 = PhotoImage(file=str(relative_to_assets("image_2.png")))
        canvas.create_image(943, 211, image=image_2)
        frame.image_2 = image_2

        # Entry for displayed position
        entry_img_1 = PhotoImage(file=str(relative_to_assets("entry_1.png")))
        canvas.create_image(470, 235, image=entry_img_1)
        entry_1 = tk.Entry(frame, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
        entry_1.place(x=370, y=205, width=200, height=58)
        entry_1.insert(0, f"{current_position[0]:.3f}")
        frame.entry_img_1 = entry_img_1

        # Entry for manual input
        entry_img_2 = PhotoImage(file=str(relative_to_assets("entry_2.png")))
        canvas.create_image(330.5, 125, image=entry_img_2)
        entry_2 = tk.Entry(frame, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
        entry_2.place(x=124, y=95, width=413, height=58)
        frame.entry_img_2 = entry_img_2

        # Button factory
        def create_button(imgp, hovp, x, y, w, h, cmd=None, toggle_idx=None):
            img = PhotoImage(file=str(relative_to_assets(imgp)))
            hov = PhotoImage(file=str(relative_to_assets(hovp)))
            btn = tk.Button(frame, image=img, borderwidth=0,
                            highlightthickness=0, relief="flat")

            def on_click():
                if toggle_idx is not None:
                    if active_button_idx[0] == toggle_idx:
                        active_button_idx[0] = None
                    else:
                        active_button_idx[0] = toggle_idx
                    update_toggle_buttons()
                if cmd:
                    cmd()

            btn.config(command=on_click)
            btn.bind("<Enter>", lambda e: btn.config(image=hov) if active_button_idx[0] != toggle_idx else None)
            btn.bind("<Leave>", lambda e: btn.config(image=img) if active_button_idx[0] != toggle_idx else None)
            btn.place(x=x, y=y, width=w, height=h)
            frame.imgs.extend([img, hov])
            return btn, img, hov

        toggle_buttons = []
        def update_toggle_buttons():
            for i,(btn,img,hov) in enumerate(toggle_buttons):
                btn.config(image=(hov if active_button_idx[0]==i else img))

        # Motion helpers
        def zero_home():
            current_position[0] = 0.0
            entry_2.delete(0, tk.END)
            entry_2.insert(0, f"{current_position[0]:.3f}")
            print("Zero pressed")

        def go_home():
            delta = -current_position[0]
            direction = "forward" if delta>0 else "backward"
            steps = int(abs(delta)/in_per_microstep)
            print(f"Home: {direction}, steps={steps}")
            if ON_PI:
                (DIR_PIN.on() if direction=="forward" else DIR_PIN.off())
                for _ in range(steps):
                    STEP_PIN.on(); time.sleep(0.001)
                    STEP_PIN.off(); time.sleep(0.001)
            zero_home()

        def move_backstop(direction):
            print(f"[DEBUG] move_backstop called, direction={direction}, toggle_idx={active_button_idx[0]}")
            idx = active_button_idx[0]
            if idx is None:
                return print("No distance selected")
            distances = [0.001,0.1,1,0.01]
            move_by = distances[idx]
            steps   = int(move_by/in_per_microstep)
            print(f"Move: {direction}, steps={steps}")
            if ON_PI:
                (DIR_PIN.on() if direction=="forward" else DIR_PIN.off())
                for _ in range(steps):
                    STEP_PIN.on(); time.sleep(0.001)
                    STEP_PIN.off(); time.sleep(0.001)
            current_position[0] += (move_by if direction=="forward" else -move_by)
            entry_2.delete(0, tk.END)
            entry_2.insert(0, f"{current_position[0]:.3f}")

        def goto_manual_position():
            try:
                target = float(entry_1.get())
            except ValueError:
                return print("Invalid manual entry")
            delta = target-current_position[0]
            direction = "forward" if delta>0 else "backward"
            steps = int(abs(delta)/in_per_microstep)
            print(f"GOTO: {direction}, steps={steps}")
            if ON_PI:
                (DIR_PIN.on() if direction=="forward" else DIR_PIN.off())
                for _ in range(steps):
                    STEP_PIN.on(); time.sleep(0.001)
                    STEP_PIN.off(); time.sleep(0.001)
            current_position[0] = target
            entry_2.delete(0, tk.END)
            entry_2.insert(0, f"{current_position[0]:.3f}")

        # Build all buttons
        frame.imgs = []
        toggle_buttons.append(create_button("button_1.png","button_hover_1.png",673,397,135,60,toggle_idx=0))
        toggle_buttons.append(create_button("button_2.png","button_hover_2.png",943,397,135,60,toggle_idx=1))
        toggle_buttons.append(create_button("button_3.png","button_hover_3.png",1078,397,135,60,toggle_idx=2))
        toggle_buttons.append(create_button("button_4.png","button_hover_4.png",808,397,135,60,toggle_idx=3))

        # Zero / Sequence / Home / Goto
        frame.imgs += create_button("button_5.png","button_hover_5.png",547,95,73,60,cmd=zero_home)
        frame.imgs += create_button("button_7.png","button_hover_6.png",215,306,300,58,cmd=lambda: switch_to("bend_sequence_setup"))
        frame.imgs += create_button("button_8.png","button_hover_7.png",215,395,300,60,cmd=go_home)
        frame.imgs += create_button("button_9.png","button_hover_8.png",608,205,150,60,cmd=goto_manual_position)
        # SWAP forward/back bindings
        frame.imgs += create_button("button_10.png","button_hover_9.png",868,307,150,60,cmd=lambda: move_backstop("backward"))
        frame.imgs += create_button("button_11.png","button_hover_10.png",868,57,150,60,cmd=lambda: move_backstop("forward"))

        # Settings nav (Exit)
        btn6 = PhotoImage(file=str(relative_to_assets("button_6.png")))
        tk.Button(frame,image=btn6,borderwidth=0,highlightthickness=0,relief="flat",
                  command=lambda: switch_to("settings")
        ).place(x=1220,y=600,width=60,height=60)
        frame.btn_img_6=btn6

    except Exception as e:
        print(f"Error loading main screen: {e}")

    return frame
