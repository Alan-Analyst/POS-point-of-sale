import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox as messagebox
from item_list import ItemList
from Pos import Pos
from about import About
from preferences import Preferences
from reports import Reports
from end_of_day import EndOfDay
from add_book import AddBook
import customtkinter as ct
from PIL import Image, ImageTk

# Connecting with the database if already exists, if it's not create a new one
with sqlite3.connect("c_bookshop_db.db") as db:
    cursor = db.cursor()

# # Create a table named Items with following fields(ID, ISBN, Title, Price)
# cursor.execute("""CREATE TABLE IF NOT EXISTS Books(id integer PRIMARY KEY, Barcode integer NOT NULL,
# Title text NOT NULL, Author text, Price float NOT NULL);""")

# Create a table named Items with following fields(ID, ISBN, Title, Price, Qty)
cursor.execute('''CREATE TABLE IF NOT EXISTS Books(id   INTEGER UNIQUE, Barcode	integer NOT NULL, 
title	text NOT NULL,
author	text,
cost_price	float,
selling_price	float NOT NULL,
qty	INTEGER NOT NULL DEFAULT 0,
cover INTEGER NOT NULL DEFAULT 0, 
copy INTEGER NOT NULL DEFAULT 0,
date_added TEXT,
PRIMARY KEY(id AUTOINCREMENT)
);''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Sales(
receipt_number	INTEGER NOT NULL UNIQUE,
date	TEXT,
cashier	TEXT,
book	TEXT,
qty	INTEGER,
price	REAL,
total	REAL,
PRIMARY KEY(receipt_number AUTOINCREMENT)
); ''')


ct.set_appearance_mode("light")  # Modes: "System" (standard), "Dark", "Light"
ct.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
ct.set_default_color_theme("dark-blue")


class Application(ct.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=2)
        self.x_height = int(self.winfo_screenwidth())
        self.y_height = int(self.winfo_screenheight())

        # Top frame
        self.frame_top = ct.CTkFrame(self, border_width=1, corner_radius=0, fg_color='white')
        self.frame_top.grid(row=0, column=0, sticky='new')

        # Center frame
        container = ct.CTkFrame(self, corner_radius=0)
        container.grid(row=1, column=0, sticky='news')
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

        self.frames = dict()

        for FrameClass in (Pos, AddBook, ItemList, Reports, Preferences, About):
            frame = FrameClass(container, self)
            self.frames[FrameClass] = frame
            frame.grid(row=0, column=0, sticky='news')

        self.show_frame(Pos)

        # Toolbox buttons
        # Make a sale button
        self.image_make_a_sale = ct.CTkImage(Image.open("images/point-of-sale.png"), size=(40, 40))
        self.btn_make_a_sale = ct.CTkButton(self.frame_top, image=self.image_make_a_sale, compound='left',
                                            text='Make a Sale', font=('arial', 16, 'bold'), height=50,
                                            command=lambda: self.show_frame(Pos))
        self.btn_make_a_sale.grid(row=0, column=0, padx=(10, 2), pady=10, ipady=3, ipadx=3)

        # Add book button
        self.image_add_book = ct.CTkImage(Image.open("images/add_book.png"), size=(40, 40))
        self.btn_item_list = ct.CTkButton(self.frame_top, text='Add Book', font=('arial', 16, 'bold'),
                                          image=self.image_add_book, compound='left', height=50,
                                          command=lambda: self.show_frame(AddBook))
        self.btn_item_list.grid(row=0, column=1, padx=2, pady=10, ipady=3, ipadx=3)

        # Item list button
        self.image_item_list = ct.CTkImage(Image.open("images/database.png"), size=(40, 40))
        self.btn_item_list = ct.CTkButton(self.frame_top, text='Inventory', font=('arial', 16, 'bold'),
                                          image=self.image_item_list, compound='left', height=50,
                                          command=lambda: self.show_frame(ItemList))
        self.btn_item_list.grid(row=0, column=2, padx=2, pady=10, ipady=3, ipadx=3)

        # Reports button
        self.image_reports = ct.CTkImage(Image.open("images/accounting.png"), size=(40, 40))
        self.btn_reports = ct.CTkButton(self.frame_top, text='Reports', font=('arial', 16, 'bold'),
                                        image=self.image_reports, compound='left', height=50,
                                        command=lambda: self.show_frame(Reports))
        self.btn_reports.grid(row=0, column=3, padx=2, pady=10, ipady=3, ipadx=3)

        # Preference button
        self.image_preferences = ct.CTkImage(Image.open("images/control.png"), size=(40, 40))
        self.btn_preferences = ct.CTkButton(self.frame_top, text='Preferences', font=('arial', 16, 'bold'),
                                            image=self.image_preferences, compound='left', height=50,
                                            command=lambda: self.show_frame(Preferences))
        self.btn_preferences.grid(row=0, column=5, padx=2, pady=10, ipady=3, ipadx=3)

        # About button
        self.image_about = ct.CTkImage(Image.open("images/about.png"), size=(40, 40))
        self.btn_about = ct.CTkButton(self.frame_top, text='About', font=('arial', 16, 'bold'), image=self.image_about,
                                      compound='left', height=50,
                                      command=lambda: self.show_frame(About))
        self.btn_about.grid(row=0, column=6, padx=2, pady=10, ipady=3, ipadx=3)

    # self.appearance_mode_label = ct.CTkLabel(self.frame_top, text="Appearance Mode:", anchor="w")
    # self.appearance_mode_label.grid(row=0, column=7, padx=7, pady=(10, 10))
    # self.appearance_mode_option_menu = ct.CTkOptionMenu(self.frame_top, values=["Light", "Dark", "System"],
    #                                                     command=self.change_appearance_mode_event, height=40)
    # self.appearance_mode_option_menu.grid(row=0, column=8, padx=4, pady=(10, 10))

    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ct.set_appearance_mode(new_appearance_mode)


# Root window
if __name__ == "__main__":
    root = Application()
    root.title('Cambridge Bookshop Point of Sale 2023')
    root.minsize(1200, 700)
    root.iconbitmap('images/point-of-sale.ico')
    root.state('zoomed')
    root.mainloop()
