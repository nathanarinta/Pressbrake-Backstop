# screens/Bend_Sequence_Setup.py
import tkinter as tk
from tkinter import Canvas, Entry, Text, Button, PhotoImage, END
from pathlib import Path
from tkinter.filedialog import asksaveasfilename, askopenfilename

def build_bend_sequence_setup(parent, show_frame_callback):
    frame = tk.Frame(parent, width=1280, height=720, bg="#FFFFFF")
    frame.step_count = 0

    # ??? Hard-coded Pi asset folder ???????????????????????????????????????????
    ASSETS_PATH = Path("/home/nathanarinta/PressGUI/assets/bend_sequence_setup/assets/frame0")

    def relative_to_assets(filename: str) -> str:
        return str(ASSETS_PATH / filename)

    # Canvas background
    canvas = tk.Canvas(
        frame,
        bg="#FFFFFF",
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0, relwidth=1, relheight=1)


    try:
        bg_img = PhotoImage(file=relative_to_assets("image_1.png"))
        canvas.create_image(640.0, 360.0, image=bg_img)
        frame._bg_image = bg_img
    except Exception as e:
        print(f"Error loading bend sequence background: {e}")

    # Titles
    canvas.create_text(275.0, 29.0, anchor="nw",
                       text="Bend Sequence Setup",
                       fill="#000000",
                       font=("IBMPlexMono Regular", -64))
    canvas.create_text(680.0, 121.0, anchor="nw",
                       text="Bend Sequence",
                       fill="#000000",
                       font=("IBMPlexMono Regular", -48))

    # Panels & headers
    canvas.create_rectangle(518.0, 201.0, 868.0, 661.0,
                            fill="#FFFFFF", outline="")
    canvas.create_rectangle(868.0, 201.0, 1218.0, 661.0,
                            fill="#FFFFFF", outline="")
    canvas.create_text(663.0, 201.0, anchor="nw",
                       text="Step", fill="#000000",
                       font=("IBMPlexMono Regular", -25))
    canvas.create_text(957.0, 201.0, anchor="nw",
                       text="Distance (in)", fill="#000000",
                       font=("IBMPlexMono Regular", -25))

    # Back button
    btn1_img = PhotoImage(file=relative_to_assets("button_1.png"))
    frame.btn1 = Button(frame, image=btn1_img,
                        borderwidth=0, highlightthickness=0,
                        relief="flat",
                        command=lambda: show_frame_callback("main"))
    frame.btn1.place(x=17.0, y=585.0, width=200.0, height=60.0)
    frame.btn1_img = btn1_img
    btn1_img_h = PhotoImage(file=relative_to_assets("button_hover_1.png"))
    frame.btn1_img_h = btn1_img_h
    frame.btn1.bind('<Enter>', lambda e: frame.btn1.config(image=btn1_img_h))
    frame.btn1.bind('<Leave>', lambda e: frame.btn1.config(image=btn1_img))

    # Load sequence
    btn2_img = PhotoImage(file=relative_to_assets("button_2.png"))
    frame.btn2 = Button(frame, image=btn2_img, borderwidth=0,
                        highlightthickness=0, relief="flat")
    frame.btn2.place(x=35.0, y=426.0, width=300.0, height=60.0)
    frame.btn2_img = btn2_img
    btn2_img_h = PhotoImage(file=relative_to_assets("button_hover_2.png"))
    frame.btn2_img_h = btn2_img_h
    frame.btn2.bind('<Enter>', lambda e: frame.btn2.config(image=btn2_img_h))
    frame.btn2.bind('<Leave>', lambda e: frame.btn2.config(image=btn2_img))
    def load_seq():
        file_path = askopenfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
            initialdir="/home/nathanarinta/PressGUI"
        )
        if not file_path:
            return
        content = Path(file_path).read_text()
        parts = content.split("||")
        steps = parts[0].splitlines() if parts else []
        dists = parts[1].splitlines() if len(parts) > 1 else []
        seq_frame = parent.frames.get("sequence_run")
        if seq_frame:
            seq_frame.entry_steps.delete("1.0", END)
            seq_frame.entry_dists.delete("1.0", END)
            for s in steps:
                seq_frame.entry_steps.insert(END, s + "\n")
            for d in dists:
                seq_frame.entry_dists.insert(END, d + "\n")
        show_frame_callback("sequence_run")
    frame.btn2.config(command=load_seq)

    # Save sequence
    btn3_img = PhotoImage(file=relative_to_assets("button_3.png"))
    frame.btn3 = Button(frame, image=btn3_img, borderwidth=0,
                        highlightthickness=0, relief="flat")
    frame.btn3.place(x=35.0, y=333.0, width=300.0, height=60.0)
    frame.btn3_img = btn3_img
    btn3_img_h = PhotoImage(file=relative_to_assets("button_hover_3.png"))
    frame.btn3_img_h = btn3_img_h
    frame.btn3.bind('<Enter>', lambda e: frame.btn3.config(image=btn3_img_h))
    frame.btn3.bind('<Leave>', lambda e: frame.btn3.config(image=btn3_img))
    def save_seq():
        steps = frame.entry_2.get("1.0", END).strip()
        dists = frame.entry_3.get("1.0", END).strip()
        data = steps + "||" + dists
        file_path = asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
            initialfile="sequence.txt",
            initialdir="/home/nathanarinta/PressGUI"
        )
        if file_path:
            Path(file_path).write_text(data)
    frame.btn3.config(command=save_seq)

    # Delete bend
    btn4_img = PhotoImage(file=relative_to_assets("button_4.png"))
    frame.btn4 = Button(frame, image=btn4_img, borderwidth=0,
                        highlightthickness=0, relief="flat")
    frame.btn4.place(x=35.0, y=240.0, width=300.0, height=60.0)
    frame.btn4_img = btn4_img
    btn4_img_h = PhotoImage(file=relative_to_assets("button_hover_4.png"))
    frame.btn4_img_h = btn4_img_h
    frame.btn4.bind('<Enter>', lambda e: frame.btn4.config(image=btn4_img_h))
    frame.btn4.bind('<Leave>', lambda e: frame.btn4.config(image=btn4_img))
    def del_bend():
        if frame.step_count > 0:
            steps_list = frame.entry_2.get("1.0", END).strip().splitlines()
            dists_list = frame.entry_3.get("1.0", END).strip().splitlines()
            steps_list.pop(); dists_list.pop()
            frame.step_count -= 1
            frame.entry_2.delete("1.0", END)
            frame.entry_3.delete("1.0", END)
            for s in steps_list:
                frame.entry_2.insert(END, s + "\n")
            for d in dists_list:
                frame.entry_3.insert(END, d + "\n")
    frame.btn4.config(command=del_bend)

    # Add bend
    btn5_img = PhotoImage(file=relative_to_assets("button_5.png"))
    frame.btn5 = Button(frame, image=btn5_img, borderwidth=0,
                        highlightthickness=0, relief="flat")
    frame.btn5.place(x=35.0, y=147.0, width=300.0, height=60.0)
    frame.btn5_img = btn5_img
    btn5_img_h = PhotoImage(file=relative_to_assets("button_hover_5.png"))
    frame.btn5_img_h = btn5_img_h
    frame.btn5.bind('<Enter>', lambda e: frame.btn5.config(image=btn5_img_h))
    frame.btn5.bind('<Leave>', lambda e: frame.btn5.config(image=btn5_img))
    def add_bend():
        dist = frame.entry_1.get().strip()
        if not dist:
            return
        frame.step_count += 1
        frame.entry_2.insert(END, f"Step {frame.step_count}\n")
        frame.entry_3.insert(END, f"{dist}\n")
        frame.entry_1.delete(0, END)
    frame.btn5.config(command=add_bend)

    # Distance input label & entry
    canvas.create_text(35.0, 510.0, anchor="nw",
                       text="Bend Dis.", fill="#000000",
                       font=("IBMPlexMono Regular", -40))
    ent1_bg = PhotoImage(file=relative_to_assets("entry_1.png"))
    canvas.create_image(368.0, 536.0, image=ent1_bg)
    frame.entry_1 = Entry(frame, bd=0, bg="#FFFFFF",
                          fg="#000716", highlightthickness=0)
    frame.entry_1.place(x=268.0, y=506.0, width=200.0, height=58.0)
    frame.entry_1_image = ent1_bg

    # Steps box
    ent2_bg = PhotoImage(file=relative_to_assets("entry_2.png"))
    canvas.create_image(693.0, 420.0, image=ent2_bg)
    frame.entry_2 = Text(frame, bd=0, bg="#D9D9D9",
                         fg="#000716", highlightthickness=0)
    frame.entry_2.place(x=528.0, y=245.0, width=330.0, height=348.0)
    frame.entry_2_image = ent2_bg

    # Distances box
    ent3_bg = PhotoImage(file=relative_to_assets("entry_3.png"))
    canvas.create_image(1043.0, 420.0, image=ent3_bg)
    frame.entry_3 = Text(frame, bd=0, bg="#D9D9D9",
                         fg="#000716", highlightthickness=0)
    frame.entry_3.place(x=878.0, y=245.0, width=330.0, height=348.0)
    frame.entry_3_image = ent3_bg

    return frame
