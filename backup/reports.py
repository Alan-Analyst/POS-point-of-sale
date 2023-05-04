import tkinter as tk
from tkinter import ttk
from style import *


class Reports(ttk.Frame):
    def __init__(self, container, controller):
        super().__init__(container)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        frame = tk.Frame(self, bg=BACKGROUND)
        frame.grid(row=0, column=0, sticky='NEWS')
