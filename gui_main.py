# noqa: E501 From: https://www.activestate.com/resources/quick-reads/how-to-display-data-in-a-table-using-tkinter/

import tkinter as tk
from ui.ui import UserInterface


if __name__ == "__main__":
    root = tk.Tk()
    ui = UserInterface(root)
    root.mainloop()
