# screens/Sequence_Run.py
import tkinter as tk
from tkinter import PhotoImage, Text
from pathlib import Path
import json, time
from hardware import STEP_PIN, DIR_PIN, ON_PI

# Path setup
HERE         = Path(__file__).resolve().parent
LOCAL_ROOT   = HERE.parent
PI_ROOT      = Path("/home/nathanarinta/PressGUI")
PROJECT_ROOT = PI_ROOT if ON_PI else LOCAL_ROOT
ASSETS_PATH  = PROJECT_ROOT / "assets" / "sequence_run" / "assets" / "frame0"

def relative_to_assets(filename: str) -> str:
    return str(ASSETS_PATH / filename)


def build_sequence_run(root, switch_to):
    frame = tk.Frame(root, bg="#FFFFFF")
    frame.current_index = 0  # track which bend is active

    # Sequence absolute position based on main screen zero
    main_frame = root.frames.get("main")
    try:
        zero_offset = main_frame.current_position[0]
    except Exception:
        zero_offset = 0.0
    frame.seq_abs_position = zero_offset

    # Canvas background
    canvas = tk.Canvas(frame, bg="#FFFFFF", bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0, relwidth=1, relheight=1)

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

    # Steps and Distances widgets
    entry_bg_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
    canvas.create_image(465.0, 277.0, image=entry_bg_1)
    entry_steps = Text(frame, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
    entry_steps.place(x=290.0, y=77.0, width=350.0, height=398.0)
    frame.entry_steps = entry_steps

    entry_bg_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
    canvas.create_image(815.0, 277.0, image=entry_bg_2)
    entry_dists = Text(frame, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
    entry_dists.place(x=640.0, y=77.0, width=350.0, height=398.0)
    frame.entry_dists = entry_dists

    # Headers
    canvas.create_text(435.0, 77.0, anchor="nw", text="Step", fill="#000000", font=("IBMPlexMono Regular", -25))
    canvas.create_text(729.0, 77.0, anchor="nw", text="Distance (in)", fill="#000000", font=("IBMPlexMono Regular", -25))

    # Highlight tag
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

    # Auto-return to zero_offset on screen open
    delta0 = zero_offset - frame.seq_abs_position
    raw0 = delta0 / in_per_microstep
    steps0 = abs(round(raw0))
    print(f"[AUTO-HOME] zero_offset={zero_offset}, seq_abs_pos={frame.seq_abs_position}, delta0={delta0}, raw0={raw0}, steps0={steps0}")
    if ON_PI and steps0 > 0:
        # positive delta => backward
        if delta0 > 0:
            DIR_PIN.on()
        else:
            DIR_PIN.off()
        for _ in range(steps0):
            STEP_PIN.on(); time.sleep(0.001)
            STEP_PIN.off(); time.sleep(0.001)
    frame.seq_abs_position = zero_offset

    # Navigate functions
    def move_to_index(idx, label):
        total = int(entry_steps.index('end-1c').split('.')[0])
        frame.current_index = idx if 1 <= idx <= total else 1
        # Highlight selection
        entry_steps.tag_remove("current", "1.0", "end")
        entry_dists.tag_remove("current", "1.0", "end")
        entry_steps.tag_add("current", f"{frame.current_index}.0", f"{frame.current_index}.end")
        entry_dists.tag_add("current", f"{frame.current_index}.0", f"{frame.current_index}.end")
        # Parse distance
        dist_line = entry_dists.get(f"{frame.current_index}.0", f"{frame.current_index}.end").strip()
        try:
            move_by = float(dist_line)
        except ValueError:
            print("Invalid distance:", dist_line)
            return
        # Compute absolute target and delta
        abs_target = zero_offset + move_by
        delta = abs_target - frame.seq_abs_position
        raw = delta / in_per_microstep
        steps_needed = abs(round(raw))
        direction = "backward" if delta > 0 else "forward"
        print(f"[{label}] move_by={move_by}, zero_offset={zero_offset}, abs_target={abs_target}, delta={delta}, raw={raw}, steps={steps_needed}, DIR={direction}")
        if ON_PI and steps_needed > 0:
            if direction == "backward":
                DIR_PIN.on()
            else:
                DIR_PIN.off()
            for _ in range(steps_needed):
                STEP_PIN.on(); time.sleep(0.001)
                STEP_PIN.off(); time.sleep(0.001)
        frame.seq_abs_position = abs_target

    def prev_bend():
        idx = frame.current_index - 1 if frame.current_index > 1 else int(entry_steps.index('end-1c').split('.')[0])
        move_to_index(idx, 'PREV')

    def next_bend():
        total = int(entry_steps.index('end-1c').split('.')[0])
        idx = frame.current_index + 1 if frame.current_index < total else 1
        move_to_index(idx, 'NEXT')

    # Buttons
    btn_prev_img = PhotoImage(file=relative_to_assets("button_1.png"))
    tk.Button(frame, image=btn_prev_img, bd=0, highlightthickness=0, relief="flat", command=prev_bend).place(x=80, y=587, width=300, height=60)
    frame.btn_prev_img = btn_prev_img

    btn_next_img = PhotoImage(file=relative_to_assets("button_2.png"))
    tk.Button(frame, image=btn_next_img, bd=0, highlightthickness=0, relief="flat", command=next_bend).place(x=495, y=587, width=300, height=60)
    frame.btn_next_img = btn_next_img

    btn_back_img = PhotoImage(file=relative_to_assets("button_3.png"))
    tk.Button(frame, image=btn_back_img, bd=0, highlightthickness=0, relief="flat",
              command=lambda: switch_to("main")).place(x=910, y=587, width=300, height=60)
    frame.btn_back_img = btn_back_img

    return frame
