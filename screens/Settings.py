# screens/settings_screen.py
import json
import tkinter as tk
from tkinter import PhotoImage
from pathlib import Path

def load_settings():
    try:
        with open("settings.json", "r") as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        return {"lead": "", "steps_per_rev": "", "micro_steps": ""}

def build_settings_screen(root, switch_to):
    frame = tk.Frame(root, bg="#FFFFFF")

    ASSETS_PATH = Path(r"C:/Users/arint/OneDrive/Desktop/Press Brake GUI/assets/settings_screen/assets/frame0")

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
        bg_img = PhotoImage(file=relative_to_assets("image_1.png"))
        canvas.create_image(640.0, 370.0, image=bg_img)
        frame.bg_img = bg_img

        canvas.create_text(
            486.0, 0.0,
            anchor="nw",
            text="Settings",
            fill="#000000",
            font=("IBMPlexMono Regular", 64 * -1)
        )

        canvas.create_text(
            504.0, 250.0,
            anchor="nw",
            text="Lead (mm)",
            fill="#000000",
            font=("IBMPlexMono Regular", 30 * -1)
        )

        canvas.create_text(
            432.0, 340.0,
            anchor="nw",
            text="Steps Per Rev",
            fill="#000000",
            font=("IBMPlexMono Regular", 30 * -1)
        )

        canvas.create_text(
            468.0, 430.0,
            anchor="nw",
            text="Micro Steps",
            fill="#000000",
            font=("IBMPlexMono Regular", 30 * -1)
        )

        settings = load_settings()

        # Entry 1
        entry_img_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
        canvas.create_image(773.0, 270.0, image=entry_img_1)
        entry_1 = tk.Entry(frame, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
        entry_1.place(x=698.0, y=240.0, width=150.0, height=58.0)
        entry_1.insert(0, settings.get("lead", ""))

        # Entry 2
        entry_img_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
        canvas.create_image(773.0, 360.0, image=entry_img_2)
        entry_2 = tk.Entry(frame, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
        entry_2.place(x=698.0, y=330.0, width=150.0, height=58.0)
        entry_2.insert(0, settings.get("steps_per_rev", ""))

        # Entry 3
        entry_img_3 = PhotoImage(file=relative_to_assets("entry_3.png"))
        canvas.create_image(773.0, 450.0, image=entry_img_3)
        entry_3 = tk.Entry(frame, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
        entry_3.place(x=698.0, y=420.0, width=150.0, height=58.0)
        entry_3.insert(0, settings.get("micro_steps", ""))

        def save_settings():
            settings = {
                "lead": entry_1.get(),
                "steps_per_rev": entry_2.get(),
                "micro_steps": entry_3.get()
            }
            with open("settings.json", "w") as f:
                json.dump(settings, f, indent=4)

        # Button 1 → Main Screen
        btn_img = PhotoImage(file=relative_to_assets("button_1.png"))
        btn_img_hover = PhotoImage(file=relative_to_assets("button_hover_1.png"))
        button = tk.Button(
            frame,
            image=btn_img,
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            command=lambda: [save_settings(), switch_to("main")]
        )
        button.place(x=489.0, y=520.0, width=300.0, height=60.0)
        frame.btn_img = btn_img
        frame.btn_img_hover = btn_img_hover

        def on_enter(e): button.config(image=btn_img_hover)
        def on_leave(e): button.config(image=btn_img)

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

    except Exception as e:
        print(f"Error loading settings screen: {e}")

    return frame
