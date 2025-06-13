import tkinter as tk
from tkinter import PhotoImage, Text
from pathlib import Path
import json, time
from hardware import STEP_PIN, DIR_PIN, ON_PI



# Path setup
HERE         = Path(__file__).resolve().parent       # .../screens
LOCAL_ROOT   = HERE.parent                            # project root when testing locally
PI_ROOT      = Path("/home/nathanarinta/PressGUI")    # Pi install path
PROJECT_ROOT = PI_ROOT if ON_PI else LOCAL_ROOT
ASSETS_PATH  = (
    PROJECT_ROOT
    / "assets"
    / "sequence_run"
    / "assets"
    / "frame0"
)

def relative_to_assets(filename: str) -> str:
    return str(ASSETS_PATH / filename)


def build_sequence_run(root, switch_to):
    frame = tk.Frame(root, bg="#FFFFFF")
    frame.current_index = 0  # track which bend is active

    # Canvas background
    canvas = tk.Canvas(
        frame, bg="#FFFFFF", height=720, width=1280,
        bd=0, highlightthickness=0, relief="ridge"
    )
    canvas.place(x=0, y=0)

    # Background image
    try:
        bg_img = PhotoImage(file=relative_to_assets("image_1.png"))
        canvas.create_image(640.0, 360.0, image=bg_img)
        frame.bg_img = bg_img
    except Exception:
        pass

    # Title
    canvas.create_text(
        452.0, 0.0, anchor="nw",
        text="Bend Sequence", fill="#000000",
        font=("IBMPlexMono Regular", -48)
    )

    # Steps Text Widget
    entry_bg_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
    canvas.create_image(465.0, 277.0, image=entry_bg_1)
    entry_steps = Text(
        frame, bd=0, bg="#FFFFFF", fg="#000716",
        highlightthickness=0
    )
    entry_steps.place(x=290.0, y=77.0, width=350.0, height=398.0)
    frame.entry_steps = entry_steps

    # Distances Text Widget
    entry_bg_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
    canvas.create_image(815.0, 277.0, image=entry_bg_2)
    entry_dists = Text(
        frame, bd=0, bg="#FFFFFF", fg="#000716",
        highlightthickness=0
    )
    entry_dists.place(x=640.0, y=77.0, width=350.0, height=398.0)
    frame.entry_dists = entry_dists

    # Header Labels
    canvas.create_text(
        435.0, 77.0, anchor="nw",
        text="Step", fill="#000000",
        font=("IBMPlexMono Regular", -25)
    )
    canvas.create_text(
        729.0, 77.0, anchor="nw",
        text="Distance (in)", fill="#000000",
        font=("IBMPlexMono Regular", -25)
    )

    # Highlight tag for current bend
    entry_steps.tag_configure("current", background="#5A99CB")
    entry_dists.tag_configure("current", background="#5A99CB")

    # Load calibration
    try:
        with open("settings.json", "r") as f:
            cfg = json.load(f)
        lead = float(cfg.get("lead", 0.0))
        spr  = int(cfg.get("steps_per_rev", 1))
        ms   = int(cfg.get("micro_steps", 1))
        in_per_microstep = lead / (spr * ms)
    except Exception as e:
        print("Settings load error:", e)
        in_per_microstep = 1.0

    # Navigate to previous bend
    def prev_bend():
        if frame.current_index > 0:
            entry_steps.tag_remove("current", f"{frame.current_index}.0", f"{frame.current_index}.end")
            entry_dists.tag_remove("current", f"{frame.current_index}.0", f"{frame.current_index}.end")
            frame.current_index -= 1
        else:
            total = int(entry_steps.index('end-1c').split('.')[0])
            frame.current_index = total

        entry_steps.tag_add("current", f"{frame.current_index}.0", f"{frame.current_index}.end")
        entry_dists.tag_add("current", f"{frame.current_index}.0", f"{frame.current_index}.end")

        dist_line = entry_dists.get(f"{frame.current_index}.0", f"{frame.current_index}.end").strip()
        try:
            move_by = float(dist_line)
        except ValueError:
            print("Invalid distance:", dist_line)
            return

        steps_needed = int(move_by / in_per_microstep)
        print(f"--> Prev Bend: DIR=backward, STEPS={steps_needed}")
        if ON_PI:
            DIR_PIN.off()  # backward
            for _ in range(steps_needed):
                STEP_PIN.on(); time.sleep(0.001)
                STEP_PIN.off(); time.sleep(0.001)

    # Navigate to next bend
    def next_bend():
        if frame.current_index > 0:
            entry_steps.tag_remove("current", f"{frame.current_index}.0", f"{frame.current_index}.end")
            entry_dists.tag_remove("current", f"{frame.current_index}.0", f"{frame.current_index}.end")

        total = int(entry_steps.index('end-1c').split('.')[0])
        frame.current_index = frame.current_index + 1 if frame.current_index < total else 1

        entry_steps.tag_add("current", f"{frame.current_index}.0", f"{frame.current_index}.end")
        entry_dists.tag_add("current", f"{frame.current_index}.0", f"{frame.current_index}.end")

        dist_line = entry_dists.get(f"{frame.current_index}.0", f"{frame.current_index}.end").strip()
        try:
            move_by = float(dist_line)
        except ValueError:
            print("Invalid distance:", dist_line)
            return

        steps_needed = int(move_by / in_per_microstep)
        print(f"--> Next Bend: DIR=forward, STEPS={steps_needed}")
        if ON_PI:
            DIR_PIN.on()  # forward
            for _ in range(steps_needed):
                STEP_PIN.on(); time.sleep(0.001)
                STEP_PIN.off(); time.sleep(0.001)

    # Buttons
    btn_prev_img = PhotoImage(file=relative_to_assets("button_1.png"))
    tk.Button(
        frame, image=btn_prev_img, bd=0, highlightthickness=0,
        relief="flat", command=prev_bend
    ).place(x=80.0, y=587.0, width=300.0, height=60.0)
    frame.btn_prev_img = btn_prev_img

    btn_next_img = PhotoImage(file=relative_to_assets("button_2.png"))
    tk.Button(
        frame, image=btn_next_img, bd=0, highlightthickness=0,
        relief="flat", command=next_bend
    ).place(x=495.0, y=587.0, width=300.0, height=60.0)
    frame.btn_next_img = btn_next_img

    btn_back_img = PhotoImage(file=relative_to_assets("button_3.png"))
    tk.Button(
        frame, image=btn_back_img, bd=0, highlightthickness=0,
        relief="flat", command=lambda: switch_to("main")
    ).place(x=910.0, y=587.0, width=300.0, height=60.0)
    frame.btn_back_img = btn_back_img

    return frame
