import tkinter as tk
from tkinter import ttk
from style import *
import customtkinter as ct


class About(ct.CTkFrame):
    def __init__(self, container, controller):
        super().__init__(container)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

