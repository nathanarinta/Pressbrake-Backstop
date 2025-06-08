import tkinter as tk
from screens.Loading_Screen import build_loading_screen
from screens.Main_Screen import build_main_screen
from screens.Bend_Sequence_Setup import build_bend_sequence_setup
from screens.Sequence_Run import build_sequence_run
from screens.Settings import build_settings_screen

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Press Brake GUI")
        self.geometry("1280x720")
        self.resizable(False, False)
        self.frames = {}

        # Initialize all screens
        self.frames["loading"] = build_loading_screen(self, self.show_frame)
        self.frames["main"] = build_main_screen(self, self.show_frame)
        self.frames["bend_sequence_setup"] = build_bend_sequence_setup(self, self.show_frame)
        self.frames["sequence_run"] = build_sequence_run(self, self.show_frame)
        self.frames["settings"] = build_settings_screen(self, self.show_frame)

        for frame in self.frames.values():
            frame.place(x=0, y=0, relwidth=1, relheight=1)

        # Show loading screen first
        self.show_frame("loading")
        self.after(2000, lambda: self.show_frame("main"))

    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()

if __name__ == "__main__":
    app = App()
    app.mainloop()
