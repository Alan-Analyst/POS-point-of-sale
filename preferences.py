import tkinter as tk
import customtkinter as ct
from tkinter import messagebox
import configparser


class Preferences(ct.CTkFrame):
    def __init__(self, container, controller):
        super().__init__(container)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Read the settings file
        config = configparser.ConfigParser()
        config.read('settings.ini')

        # Get the values
        self.cashier_name = config.get('info', 'cashier')
        self.shop_name = config.get('info', 'shop')
        self.address = config.get('info', 'address')
        self.phone = config.get('info', 'phone')

        # Information frame
        self.frame_info = ct.CTkFrame(self, fg_color='white')
        self.frame_info.grid(row=0, column=0, padx=10, pady=10, sticky='NWE')
        self.frame_info.columnconfigure(0, weight=1)
        self.frame_info.columnconfigure(1, weight=1)
        self.frame_info.columnconfigure(2, weight=1)

        # Cashier Name
        self.lbl_cashier = ct.CTkLabel(self.frame_info, text=f'Cashier Name: {self.cashier_name}',
                                       font=ct.CTkFont(size=18))
        self.lbl_cashier.grid(row=0, column=0, padx=10, pady=10, sticky='W')

        self.ent_cashier = ct.CTkEntry(self.frame_info, width=350)
        self.ent_cashier.grid(row=0, column=1, padx=10, pady=10, sticky='WE')

        # Shop Name
        self.lbl_shop = ct.CTkLabel(self.frame_info, text=f'Shop Name: {self.shop_name}', font=ct.CTkFont(size=18))
        self.lbl_shop.grid(row=1, column=0, padx=10, pady=10, sticky='W')

        self.ent_shop = ct.CTkEntry(self.frame_info, width=350)
        self.ent_shop.grid(row=1, column=1, padx=10, pady=10, sticky='WE')

        # Address
        self.lbl_address = ct.CTkLabel(self.frame_info, text=f'Address: {self.address}', font=ct.CTkFont(size=18))
        self.lbl_address.grid(row=2, column=0, padx=10, pady=10, sticky='W')

        self.ent_address = ct.CTkEntry(self.frame_info, width=350)
        self.ent_address.grid(row=2, column=1, padx=10, pady=10, sticky='WE')

        # Phone Number
        self.lbl_phone = ct.CTkLabel(self.frame_info, text=f'Phone Number: {self.phone}', font=ct.CTkFont(size=18))
        self.lbl_phone.grid(row=3, column=0, padx=10, pady=10, sticky='W')

        self.ent_phone = ct.CTkEntry(self.frame_info, width=350)
        self.ent_phone.grid(row=3, column=1, padx=10, pady=10, sticky='WE')

        self.switch_var = ct.StringVar(value=config.get('settings', 'switch'))

        switch_1 = ct.CTkSwitch(self.frame_info, text="Full Screen Mode", command=self.switch_event,
                                variable=self.switch_var, onvalue="on", offvalue="off")
        switch_1.grid(row=0, column=2, padx=10, pady=10, sticky='W')

        # Button
        self.btn_save_change = ct.CTkButton(self.frame_info, text='Change', height=40, command=self.save)
        self.btn_save_change.grid(row=1, column=2, padx=10, pady=10, sticky='WE')

    def switch_event(self):
        # Read the settings file
        config = configparser.ConfigParser()
        config.read('settings.ini')

        if self.switch_var.get() == 'on':
            # Change to full screen mode
            config.set('settings', 'full_screen', 'True')
            config.set('settings', 'switch', 'on')
        else:
            config.set('settings', 'full_screen', 'False')
            config.set('settings', 'switch', 'off')

        # Write the updated settings to the file
        with open('settings.ini', 'w') as configfile:
            config.write(configfile)

    def save(self):
        # Read the settings file
        config = configparser.ConfigParser()
        config.read('settings.ini')
        lengths = [self.ent_cashier, self.ent_shop, self.ent_address,
                   self.ent_phone]
        for length in lengths:
            if len(length.get()) > 35:
                messagebox.showwarning('Oops!', f'{length.get()} Exceeded maximum length of 36 characters!')
                return
        if self.ent_cashier.get():
            # Update the cashier variable
            config.set('info', 'cashier', self.ent_cashier.get().strip())
        if self.ent_shop.get():
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
