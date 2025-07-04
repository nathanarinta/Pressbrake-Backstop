# screens/Sequence_Run.py
import tkinter as tk
from tkinter import PhotoImage, Text
from pathlib import Path
import json
import time
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
    frame.current_index = 0  # which step is highlighted
    frame.seq_zero = None    # baseline zero for this session

    # Load calibration once
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

    # Canvas setup
    canvas = tk.Canvas(frame, bg="#FFFFFF", bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0, relwidth=1, relheight=1)
    try:
        bg = PhotoImage(file=relative_to_assets("image_1.png"))
        canvas.create_image(640, 360, image=bg)
        frame.bg_img = bg
    except:
        pass

    canvas.create_text(452, 0, anchor="nw", text="Bend Sequence", fill="#000000",
                       font=("IBMPlexMono Regular", -48))

    # Steps widget
    steps_bg = PhotoImage(file=relative_to_assets("entry_1.png"))
    canvas.create_image(465, 277, image=steps_bg)
    entry_steps = Text(frame, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
    entry_steps.place(x=290, y=77, width=350, height=398)
    frame.entry_steps = entry_steps

    # Distances widget
    dists_bg = PhotoImage(file=relative_to_assets("entry_2.png"))
    canvas.create_image(815, 277, image=dists_bg)
    entry_dists = Text(frame, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
    entry_dists.place(x=640, y=77, width=350, height=398)
    frame.entry_dists = entry_dists

    # Headers
    canvas.create_text(435, 77, anchor="nw", text="Step", fill="#000000",
                       font=("IBMPlexMono Regular", -25))
    canvas.create_text(729, 77, anchor="nw", text="Distance (in)", fill="#000000",
                       font=("IBMPlexMono Regular", -25))

    # Highlight tag
    entry_steps.tag_configure("current", background="#5A99CB")
    entry_dists.tag_configure("current", background="#5A99CB")

    # Reset: clear highlight/index and capture baseline zero
    def reset_sequence():
        main = root.frames["main"]
        # capture baseline zero
        frame.seq_zero = main.current_position[0]
        # clear highlight and index
        frame.current_index = 0
        entry_steps.tag_remove("current", "1.0", "end")
        entry_dists.tag_remove("current", "1.0", "end")
        # home if needed
        current_real = main.current_position[0]
        delta = frame.seq_zero - current_real
        steps = abs(round(delta / in_per_microstep))
        if ON_PI and steps > 0:
            (DIR_PIN.on() if delta > 0 else DIR_PIN.off())
            for _ in range(steps):
                STEP_PIN.on(); time.sleep(0.001)
                STEP_PIN.off(); time.sleep(0.001)
        # update global tracker
        main.current_position[0] = frame.seq_zero
    frame.reset_sequence = reset_sequence

    # Move helper: use seq_zero as baseline
    def move_to_index(idx, label):
        main = root.frames["main"]
        zero = frame.seq_zero  # fixed baseline
        # wrap idx
        total = int(entry_steps.index('end-1c').split('.')[0])
        frame.current_index = idx if 1 <= idx <= total else 1
        # highlight
        entry_steps.tag_remove("current", "1.0", "end")
        entry_dists.tag_remove("current", "1.0", "end")
        entry_steps.tag_add("current", f"{frame.current_index}.0", f"{frame.current_index}.end")
        entry_dists.tag_add("current", f"{frame.current_index}.0", f"{frame.current_index}.end")
        # parse distance (absolute from zero)
        dist_line = entry_dists.get(f"{frame.current_index}.0", f"{frame.current_index}.end").strip()
        try:
            move_by = float(dist_line)
        except ValueError:
            print("Invalid distance:", dist_line)
            return
        # target absolute
        target = zero + move_by
        current_real = main.current_position[0]
        delta = target - current_real
        steps = abs(round(delta / in_per_microstep))
        direction = "backward" if delta > 0 else "forward"
        print(f"[{label}] step={frame.current_index}, zero={zero:.3f}, "
              f"current={current_real:.3f}, move_by={move_by:.3f}, delta={delta:.3f}, steps={steps}")
        # motor pulses
        if ON_PI and steps > 0:
            (DIR_PIN.on() if direction == "backward" else DIR_PIN.off())
            for _ in range(steps):
                STEP_PIN.on(); time.sleep(0.001)
                STEP_PIN.off(); time.sleep(0.001)
        # update global position
        main.current_position[0] = target

    def prev_bend():
        idx = frame.current_index - 1 if frame.current_index > 1 else \
              int(entry_steps.index('end-1c').split('.')[0])
        move_to_index(idx, 'PREV')

    def next_bend():
        total = int(entry_steps.index('end-1c').split('.')[0])
        idx = frame.current_index + 1 if frame.current_index < total else 1
        move_to_index(idx, 'NEXT')

    # Buttons
    btn_prev = PhotoImage(file=relative_to_assets("button_1.png"))
    tk.Button(frame, image=btn_prev, bd=0, highlightthickness=0, relief="flat",
              command=prev_bend).place(x=80, y=587, width=300, height=60)
    frame.btn_prev_img = btn_prev

    btn_next = PhotoImage(file=relative_to_assets("button_2.png"))
    tk.Button(frame, image=btn_next, bd=0, highlightthickness=0, relief="flat",
              command=next_bend).place(x=495, y=587, width=300, height=60)
    frame.btn_next_img = btn_next

    btn_back = PhotoImage(file=relative_to_assets("button_3.png"))
    tk.Button(frame, image=btn_back, bd=0, highlightthickness=0, relief="flat",
              command=lambda: switch_to("main")).place(x=910, y=587, width=300, height=60)
    frame.btn_back_img = btn_back

    return frame
