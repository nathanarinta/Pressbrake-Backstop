# screens/loading_screen.py
import tkinter as tk
from tkinter import PhotoImage
from pathlib import Path

def build_loading_screen(root, switch_to):
    frame = tk.Frame(root, bg="#FFFFFF")

    # ??? HARD-CODED ASSET PATH FOR YOUR PI ????????????????????????????????????
    ASSETS_PATH = Path("/home/nathanarinta/PressGUI/assets/loading_screen/assets/frame0")

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / path

    canvas = tk.Canvas(
        frame,
        bg="#FFFFFF",
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0, relwidth=1, relheight=1)


    try:
        # note the str(...) here so PhotoImage always gets a string
        image_1 = PhotoImage(file=str(relative_to_assets("image_1.png")))
        image_2 = PhotoImage(file=str(relative_to_assets("image_2.png")))
        image_3 = PhotoImage(file=str(relative_to_assets("image_3.png")))

        canvas.create_image(640.0, 360.0, image=image_1)
        canvas.create_image(639.0, 608.0, image=image_2)
        canvas.create_image(640.0, 263.0, image=image_3)

        # prevent Python GC from reclaiming these images
        frame.image_1 = image_1
        frame.image_2 = image_2
        frame.image_3 = image_3

    except Exception as e:
        print(f"Error loading loading screen assets: {e}")

    return frame
