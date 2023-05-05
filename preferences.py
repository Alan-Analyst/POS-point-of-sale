import tkinter as tk
from tkinter import ttk
import customtkinter as ct
from tkinter import messagebox
import configparser


class Preferences(ct.CTkFrame):
    def __init__(self, container, controller):
        super().__init__(container)

        # Read the settings file
        config = configparser.ConfigParser()
        config.read('settings.ini')

        # Get the values
        self.cashier_name = config.get('info', 'cashier')
        self.shop_name = config.get('info', 'shop')
        self.address = config.get('info', 'address')
        self.phone = config.get('info', 'phone')

        # Cashier Name
        self.lbl_cashier = ct.CTkLabel(self, text=f'Cashier Name: {self.cashier_name}', font=ct.CTkFont(size=18))
        self.lbl_cashier.grid(row=0, column=0, padx=10, pady=10, sticky='W')

        self.ent_cashier = ct.CTkEntry(self)
        self.ent_cashier.grid(row=0, column=1, padx=10, pady=10, sticky='W')

        # Shop Name
        self.lbl_shop = ct.CTkLabel(self, text=f'Shop Name: {self.shop_name}', font=ct.CTkFont(size=18))
        self.lbl_shop.grid(row=1, column=0, padx=10, pady=10, sticky='W')

        self.ent_shop = ct.CTkEntry(self)
        self.ent_shop.grid(row=1, column=1, padx=10, pady=10, sticky='W')

        # Address
        self.lbl_address = ct.CTkLabel(self, text=f'Address: {self.address}', font=ct.CTkFont(size=18))
        self.lbl_address.grid(row=4, column=0, padx=10, pady=10, sticky='W')

        self.ent_address = ct.CTkEntry(self)
        self.ent_address.grid(row=4, column=1, padx=10, pady=10, sticky='W')

        # Phone Number
        self.lbl_phone = ct.CTkLabel(self, text=f'Phone Number: {self.phone}', font=ct.CTkFont(size=18))
        self.lbl_phone.grid(row=3, column=0, padx=10, pady=10, sticky='W')

        self.ent_phone = ct.CTkEntry(self)
        self.ent_phone.grid(row=3, column=1, padx=10, pady=10, sticky='W')

        # Button
        self.btn_save_change = ct.CTkButton(self, text='Change', height=40, command=self.save)
        self.btn_save_change.grid(row=5, column=1, padx=10, pady=10, sticky='W')

    def save(self):
        # Read the settings file
        config = configparser.ConfigParser()
        config.read('settings.ini')

        if self.ent_cashier.get():
            # Update the cashier variable
            config.set('info', 'cashier', self.ent_cashier.get().strip())
        if self.ent_phone.get():
            # Update the shop variable
            config.set('info', 'shop', self.ent_shop.get().strip())
        if self.ent_address.get():
            # Update the address variable
            config.set('info', 'address', self.ent_address.get().strip())
        if self.ent_phone.get():
            # Update the phone variable
            config.set('info', 'phone', self.ent_phone.get().strip())

        # Write the updated settings to the file
        with open('settings.ini', 'w') as configfile:
            config.write(configfile)

        # Read the settings file
        config = configparser.ConfigParser()
        config.read('settings.ini')

        # Get the values
        self.cashier_name = config.get('info', 'cashier')
        self.shop_name = config.get('info', 'shop')
        self.address = config.get('info', 'address')
        self.phone = config.get('info', 'phone')

        self.lbl_cashier.configure(text=f'Cashier Name: {self.cashier_name}')
        self.lbl_shop.configure(text=f'Shop Name: {self.shop_name}')
        self.lbl_address.configure(text=f'Address: {self.address}')
        self.lbl_phone.configure(text=f'Phone Number: {self.phone}')
        messagebox.showinfo('Success!', "Changes saved! Please restart to apply change.")
        self.ent_cashier.delete(0, tk.END)
        self.ent_shop.delete(0, tk.END)
        self.ent_address.delete(0, tk.END)
        self.ent_phone.delete(0, tk.END)



