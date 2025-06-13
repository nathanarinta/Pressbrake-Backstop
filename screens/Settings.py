# screens/settings_screen.py
import json
import tkinter as tk
from tkinter import PhotoImage
from pathlib import Path

def build_settings_screen(root, switch_to):
    frame = tk.Frame(root, bg="#FFFFFF")

    # ??? Hard-coded Pi asset folder ???????????????????????????????????????????
    ASSETS_PATH = Path("/home/nathanarinta/PressGUI/assets/settings_screen/assets/frame0")

    def relative_to_assets(filename: str) -> Path:
        return ASSETS_PATH / filename

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
        # Background
        bg_img = PhotoImage(file=str(relative_to_assets("image_1.png")))
        canvas.create_image(640.0, 370.0, image=bg_img)
        frame.bg_img = bg_img

        # Headings
        canvas.create_text(
            486.0, 0.0,
            anchor="nw",
            text="Settings",
            fill="#000000",
            font=("IBMPlexMono Regular", -64)
        )

        canvas.create_text(
            504.0, 250.0,
            anchor="nw",
            text="Lead (mm)",
            fill="#000000",
            font=("IBMPlexMono Regular", -30)
        )

        canvas.create_text(
            432.0, 340.0,
            anchor="nw",
            text="Steps Per Rev",
            fill="#000000",
            font=("IBMPlexMono Regular", -30)
        )

        canvas.create_text(
            468.0, 430.0,
            anchor="nw",
            text="Micro Steps",
            fill="#000000",
            font=("IBMPlexMono Regular", -30)
        )

        # Load existing settings
        try:
            with open("settings.json", "r") as f:
                settings = json.load(f)
        except FileNotFoundError:
            settings = {"lead": "", "steps_per_rev": "", "micro_steps": ""}

        # Entry fields
        entry_img_1 = PhotoImage(file=str(relative_to_assets("entry_1.png")))
        canvas.create_image(773.0, 270.0, image=entry_img_1)
        entry_1 = tk.Entry(frame, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
        entry_1.place(x=698.0, y=240.0, width=150.0, height=58.0)
        entry_1.insert(0, settings.get("lead", ""))

        entry_img_2 = PhotoImage(file=str(relative_to_assets("entry_2.png")))
        canvas.create_image(773.0, 360.0, image=entry_img_2)
        entry_2 = tk.Entry(frame, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
        entry_2.place(x=698.0, y=330.0, width=150.0, height=58.0)
        entry_2.insert(0, settings.get("steps_per_rev", ""))

        entry_img_3 = PhotoImage(file=str(relative_to_assets("entry_3.png")))
        canvas.create_image(773.0, 450.0, image=entry_img_3)
        entry_3 = tk.Entry(frame, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
        entry_3.place(x=698.0, y=420.0, width=150.0, height=58.0)
        entry_3.insert(0, settings.get("micro_steps", ""))

        # Save settings callback
        def save_settings():
            new_settings = {
                "lead": entry_1.get(),
                "steps_per_rev": entry_2.get(),
                "micro_steps": entry_3.get()
            }
            with open("settings.json", "w") as f:
                json.dump(new_settings, f, indent=4)

        # Save & Back button
        btn_img       = PhotoImage(file=str(relative_to_assets("button_1.png")))
        btn_img_hover = PhotoImage(file=str(relative_to_assets("button_hover_1.png")))
        button = tk.Button(
            frame,
            image=btn_img,
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            command=lambda: [save_settings(), switch_to("main")]
        )
        button.place(x=489.0, y=520.0, width=300.0, height=60.0)
        frame.btn_img       = btn_img
        frame.btn_img_hover = btn_img_hover

        button.bind("<Enter>", lambda e: button.config(image=btn_img_hover))
        button.bind("<Leave>", lambda e: button.config(image=btn_img))

    except Exception as e:
        print(f"Error loading settings screen: {e}")

    return frame
