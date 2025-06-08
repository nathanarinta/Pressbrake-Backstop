# screens/sequence_run.py
import tkinter as tk
from tkinter import PhotoImage, Text
from pathlib import Path

def build_sequence_run(root, switch_to):
    frame = tk.Frame(root, bg="#FFFFFF")

    ASSETS_PATH = Path(r"C:/Users/arint/OneDrive/Desktop/Press Brake GUI/assets/sequence_run/assets/frame0")

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
        image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
        canvas.create_image(640.0, 360.0, image=image_1)
        frame.image_1 = image_1

        canvas.create_text(
            452.0,
            0.0,
            anchor="nw",
            text="Bend Sequence",
            fill="#000000",
            font=("IBMPlexMono Regular", 48 * -1)
        )

        # Entry Fields
        entry_bg_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
        canvas.create_image(465.0, 277.0, image=entry_bg_1)
        entry_1 = Text(frame, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
        entry_1.place(x=290.0, y=77.0, width=350.0, height=398.0)
        frame.entry_1 = entry_1

        entry_bg_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
        canvas.create_image(815.0, 277.0, image=entry_bg_2)
        entry_2 = Text(frame, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
        entry_2.place(x=640.0, y=77.0, width=350.0, height=398.0)
        frame.entry_2 = entry_2

        canvas.create_text(
            729.0, 77.0,
            anchor="nw",
            text="Distance (in)",
            fill="#000000",
            font=("IBMPlexMono Regular", 25 * -1)
        )

        canvas.create_text(
            435.0, 77.0,
            anchor="nw",
            text="Step",
            fill="#000000",
            font=("IBMPlexMono Regular", 25 * -1)
        )

        # Button 1: Placeholder (you can replace with logic later)
        btn_img_1 = PhotoImage(file=relative_to_assets("button_1.png"))
        button_1 = tk.Button(
            frame,
            image=btn_img_1,
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            command=lambda: print("Start Sequence")
        )
        button_1.place(x=80.0, y=587.0, width=300.0, height=60.0)
        frame.btn_img_1 = btn_img_1

        # Button 2: Placeholder
        btn_img_2 = PhotoImage(file=relative_to_assets("button_2.png"))
        button_2 = tk.Button(
            frame,
            image=btn_img_2,
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            command=lambda: print("Next Bend")
        )
        button_2.place(x=495.0, y=587.0, width=300.0, height=60.0)
        frame.btn_img_2 = btn_img_2

        # Button 3: Back to Main
        btn_img_3 = PhotoImage(file=relative_to_assets("button_3.png"))
        button_3 = tk.Button(
            frame,
            image=btn_img_3,
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            command=lambda: switch_to("main")
        )
        button_3.place(x=910.0, y=587.0, width=300.0, height=60.0)
        frame.btn_img_3 = btn_img_3

    except Exception as e:
        print(f"Error loading sequence run screen: {e}")

    return frame
