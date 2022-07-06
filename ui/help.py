from tkinter import ttk
import tkinter as tk


class AboutDialog:
    def __init__(self, parent, program_name):
        self.parent = parent
        self.program_name = program_name
        # Set up new window.
        self.about_box = tk.Toplevel(self.parent)
        self.about_box.title("About " + self.program_name)
        self.about_box.geometry("400x300")
        self.about_box.grid_rowconfigure(0, pad=10, weight=1)
        self.about_box.grid_columnconfigure(0, pad=10, weight=1)
        frame = tk.Frame(self.about_box, borderwidth=4, relief="ridge")
        # The shows the frame the same size as the window.
        frame.grid(sticky="nesw")
        # Label frame
        label_frame = tk.LabelFrame(frame, text="About this program...")
        label_frame.grid(column=0, row=0, columnspan=3, rowspan=3, sticky=("nesw"))
        display_string = self.program_name + " is AWESOME!"
        label = ttk.Label(label_frame, text=display_string)
        label.grid(column=1, row=1, sticky="n", padx=5, pady=5)
        # OK button
        self.ok_button = tk.Button(frame, text="OK", command=self.exit)
        self.ok_button.grid(column=1, row=3, sticky="s")

    def exit(self):
        # Quit dialog doing nothing.
        self.about_box.destroy()
