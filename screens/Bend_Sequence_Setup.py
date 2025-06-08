# screens/bend_sequence_setup.py
import tkinter as tk
from tkinter import PhotoImage, Entry
from pathlib import Path

def build_bend_sequence_setup(root, switch_to):
    frame = tk.Frame(root, bg="#FFFFFF")

    ASSETS_PATH = Path(r"C:/Users/arint/OneDrive/Desktop/Press Brake GUI/assets/bend_sequence_setup/assets/frame0")

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
        canvas.create_image(640, 360, image=image_1)
        frame.image_1 = image_1

        canvas.create_text(275.0, 29.0, anchor="nw", text="Bend Sequence Setup", fill="#000000", font=("IBMPlexMono Regular", 64))
        canvas.create_text(660.0, 180.0, anchor="nw", text="Bend Sequence", fill="#000000", font=("IBMPlexMono Regular", 48))

        canvas.create_rectangle(518.0, 261.0, 868.0, 661.0, fill="#FFFFFF", outline="")
        canvas.create_rectangle(868.0, 261.0, 1218.0, 661.0, fill="#FFFFFF", outline="")

        canvas.create_text(957.0, 261.0, anchor="nw", text="Distance (in)", fill="#000000", font=("IBMPlexMono Regular", 25))
        canvas.create_text(663.0, 261.0, anchor="nw", text="Step", fill="#000000", font=("IBMPlexMono Regular", 25))
        canvas.create_text(35.0, 570.0, anchor="nw", text="Bend Dis.", fill="#000000", font=("IBMPlexMono Regular", 40))

        entry_img_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
        canvas.create_image(368.0, 596.0, image=entry_img_1)
        frame.entry_img_1 = entry_img_1

        entry_1 = Entry(frame, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
        entry_1.place(x=268.0, y=566.0, width=200.0, height=58.0)

        def create_button(x, y, width, height, img, hover_img, command):
            button = tk.Button(frame, image=img, borderwidth=0, highlightthickness=0, relief="flat", command=command)
            button.place(x=x, y=y, width=width, height=height)
            def on_enter(e): button.config(image=hover_img)
            def on_leave(e): button.config(image=img)
            button.bind('<Enter>', on_enter)
            button.bind('<Leave>', on_leave)
            return button

        btn_images = {}
        for i in range(1, 6):
            btn_images[f"img_{i}"] = PhotoImage(file=relative_to_assets(f"button_{i}.png"))
            btn_images[f"hover_{i}"] = PhotoImage(file=relative_to_assets(f"button_hover_{i}.png"))

        frame.btn_1 = create_button(17, 645, 200, 60, btn_images["img_1"], btn_images["hover_1"], lambda: switch_to("main"))
        frame.btn_2 = create_button(35, 486, 300, 60, btn_images["img_2"], btn_images["hover_2"], lambda: switch_to("sequence_run"))
        frame.btn_3 = create_button(35, 393, 300, 60, btn_images["img_3"], btn_images["hover_3"], lambda: print("Delete Selected"))
        frame.btn_4 = create_button(35, 300, 300, 60, btn_images["img_4"], btn_images["hover_4"], lambda: print("Save Sequence"))
        frame.btn_5 = create_button(35, 207, 300, 60, btn_images["img_5"], btn_images["hover_5"], lambda: print("Load Sequence"))

    except Exception as e:
        print(f"Error loading bend sequence setup assets: {e}")

    return frame
