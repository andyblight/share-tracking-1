from tkinter import ttk
import tkinter as tk


# FIXME Get program name from single point.
__program_name__ = "Share Tracker"

class HelpMenu(tk.Menu):
    def __init__(self, parent, menu_bar):
        self.parent = parent
        self.menu_help = tk.Menu(menu_bar)
        self.menu_help.add_command(label="Help Index", command=self.do_nothing)
        self.menu_help.add_command(label="About...", command=self.dialog_about)
        menu_bar.add_cascade(label="Help", menu=self.menu_help)

    def do_nothing(self):
        pass

    def dialog_about_exit(self):
        self.about_box.destroy()

    def dialog_about(self):
        self.about_box = tk.Toplevel(self.parent)
        self.about_box.title("About " + __program_name__)
        self.about_box.geometry("400x300")
        self.about_box.grid_rowconfigure(0, pad=10, weight=1)
        self.about_box.grid_columnconfigure(0, pad=10, weight=1)
        frame = tk.Frame(self.about_box, borderwidth=4, relief="ridge")
        # The shows the frame the same size as the window.
        frame.grid(sticky="nesw")

        # Label frame
        label_frame = tk.LabelFrame(frame, text="About this program...")
        label_frame.grid(column=0, row=0, columnspan=3, rowspan=3, sticky=("nesw"))
        display_string = __program_name__ + " is AWESOME!"
        label = ttk.Label(label_frame, text=display_string)
        label.grid(column=1, row=1, sticky="n", padx=5, pady=5)

        self.ok_button = tk.Button(frame, text="OK", command=self.dialog_about_exit)
        self.ok_button.grid(column=1, row=3, sticky="s")


