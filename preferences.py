import tkinter as tk
from tkinter import ttk
from style import *
import customtkinter as ct
from tkinter import messagebox


class Preferences(ct.CTkFrame):
    def __init__(self, container, controller):
        super().__init__(container)

        with open('settings.ini', 'r') as f:
            self.cashier_name = f.read()

        self.lbl = ct.CTkLabel(self, text=f'Cashier Name: {self.cashier_name}', font=ct.CTkFont(size=18))
        self.lbl.grid(row=0, column=0, padx=10, pady=10)

        self.button = ct.CTkButton(self, text='Change', command=self.save, height=40)
        self.button.grid(row=0, column=1, padx=10, pady=10)

    def save(self):
        dialog = ct.CTkInputDialog(text="Type the Cashier's name:", title="Change Cashier")
        self.cashier_name = str(dialog.get_input())
        with open('settings.ini', 'w') as setting:
            setting.write(self.cashier_name)
        self.lbl.configure(text=f'Cashier Name: {self.cashier_name}')
        messagebox.showinfo('Success!', "Cashier's name changed successfully! Please restart to apply change.")



