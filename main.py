import sqlite3
from item_list import ItemList
from Pos import Pos
from about import About
from preferences import Preferences
from reports import Reports
from add_book import AddBook
import customtkinter as ct
from PIL import Image
import configparser

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
category TEXT,
PRIMARY KEY(id AUTOINCREMENT)
);''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Sales(
receipt_number	INTEGER NOT NULL,
date	TEXT,
cashier	TEXT,
book	TEXT,
qty	INTEGER,
price	REAL,
total	REAL
); ''')


ct.set_appearance_mode("light")  # Modes: "System" (standard), "Dark", "Light"
ct.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


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
        self.frame_top.columnconfigure(7, weight=1)

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
        self.img_make_a_sale = ct.CTkImage(Image.open("images/point-of-sale.png"), size=(40, 40))
        self.btn_make_a_sale = ct.CTkButton(self.frame_top, image=self.img_make_a_sale, compound='left',
                                            text='Make a Sale', font=('arial', 16, 'bold'), height=50,
                                            command=lambda: self.show_frame(Pos))
        self.btn_make_a_sale.grid(row=0, column=0, padx=(10, 2), pady=10, ipady=3, ipadx=3)

        # Add book button
        self.img_add_book = ct.CTkImage(Image.open("images/add_book.png"), size=(40, 40))
        self.btn_item_list = ct.CTkButton(self.frame_top, text='Add Book', font=('arial', 16, 'bold'),
                                          image=self.img_add_book, compound='left', height=50,
                                          command=lambda: self.show_frame(AddBook))
        self.btn_item_list.grid(row=0, column=1, padx=2, pady=10, ipady=3, ipadx=3)

        # Item list button
        self.img_item_list = ct.CTkImage(Image.open("images/database.png"), size=(40, 40))
        self.btn_item_list = ct.CTkButton(self.frame_top, text='Inventory', font=('arial', 16, 'bold'),
                                          image=self.img_item_list, compound='left', height=50,
                                          command=lambda: self.show_frame(ItemList))
        self.btn_item_list.grid(row=0, column=2, padx=2, pady=10, ipady=3, ipadx=3)

        # Reports button
        self.img_reports = ct.CTkImage(Image.open("images/reports.png"), size=(40, 40))
        self.btn_reports = ct.CTkButton(self.frame_top, text='Reports', font=('arial', 16, 'bold'),
                                        image=self.img_reports, compound='left', height=50,
                                        command=lambda: self.show_frame(Reports))
        self.btn_reports.grid(row=0, column=3, padx=2, pady=10, ipady=3, ipadx=3)

        # Preference button
        self.img_preferences = ct.CTkImage(Image.open("images/preferences.png"), size=(40, 40))
        self.btn_preferences = ct.CTkButton(self.frame_top, text='Preferences', font=('arial', 16, 'bold'),
                                            image=self.img_preferences, compound='left', height=50,
                                            command=lambda: self.show_frame(Preferences))
        self.btn_preferences.grid(row=0, column=5, padx=2, pady=10, ipady=3, ipadx=3)

        # About button
        self.img_about = ct.CTkImage(Image.open("images/about.png"), size=(40, 40))
        self.btn_about = ct.CTkButton(self.frame_top, text='About', font=('arial', 16, 'bold'), image=self.img_about,
                                      compound='left', height=50,
                                      command=lambda: self.show_frame(About))
        self.btn_about.grid(row=0, column=6, padx=2, pady=10, ipady=3, ipadx=3)

        # Exit button
        self.img_exit = ct.CTkImage(Image.open("images/exit.png"), size=(40, 40))
        self.btn_exit = ct.CTkButton(self.frame_top, text='X', font=('arial', 28, 'bold'),
                                     compound='left', height=53, width=38, fg_color='#E74C3C', text_color='white',
                                     hover_color='red',
                                     command=lambda: root.destroy())
        self.btn_exit.grid(row=0, column=7, padx=10, pady=10, sticky='e')

    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()


# Root window
if __name__ == "__main__":
    root = Application()

    # Read the settings file
    config = configparser.ConfigParser()
    config.read('settings.ini')

    root.title(f'{config.get("info", "shop")} Point of Sale 2023')

    root.iconbitmap('images/point-of-sale.ico')
    # set the window state to full screen
    if config.get("settings", "full_screen") == 'True':
        root.overrideredirect(True)
    else:
        root.overrideredirect(False)

    # get the width and height of the screen
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # set the size and position of the window to cover the entire screen
    root.geometry("%dx%d+0+0" % (screen_width, screen_height))
    root.minsize(980, 700)
    root.mainloop()
