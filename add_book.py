import tkinter as tk
from tkinter import ttk
import customtkinter as ct
from tkinter import messagebox
import datetime
import sqlite3
from item_list import ItemList

# Connecting with the database if already exists, if it's not create a new one
with sqlite3.connect("c_bookshop_db.db") as db:
    cursor = db.cursor()


class AddBook(ct.CTkFrame):
    def __init__(self, container, controller):
        super().__init__(container)

        self.grid(row=0, column=0, sticky='NEWS')
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.configure(fg_color='transparent')

        frame = ct.CTkFrame(self, corner_radius=0)
        frame.grid(row=0, column=0, sticky='NEWS')
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        frame_center = ct.CTkFrame(frame, corner_radius=0, fg_color='transparent')
        frame_center.grid(sticky=(tk.E + tk.W + tk.S + tk.N))
        frame_center.columnconfigure(0, weight=1)
        frame_center.rowconfigure(0, weight=0)
        frame_center.rowconfigure(1, weight=1)

        sub_frame_scan_book1 = ct.CTkFrame(frame_center, fg_color='transparent')
        sub_frame_scan_book1.grid(sticky=(tk.W + tk.E + tk.N + tk.S))
        for i in range(3):
            sub_frame_scan_book1.columnconfigure(i, weight=1)
        sub_frame_scan_book1.rowconfigure(2, weight=0)
        sub_frame_scan_book1.rowconfigure(3, weight=0)

        main_frame2 = ct.CTkFrame(frame_center, fg_color='transparent')
        main_frame2.grid(sticky=(tk.W + tk.E + tk.S + tk.N), padx=10)
        main_frame2.columnconfigure(0, weight=1)
        main_frame2.rowconfigure(0, weight=1)

        # Data entry labels
        self.barcode = tk.StringVar()
        ct.CTkLabel(sub_frame_scan_book1, text='Barcode').grid(row=0, column=0)
        self.barcode_entry = ct.CTkEntry(sub_frame_scan_book1, textvariable=self.barcode)
        self.barcode_entry.grid(row=1, column=0, sticky=(tk.W + tk.E), padx=(10, 2))

        self.title = tk.StringVar()
        ct.CTkLabel(sub_frame_scan_book1, text='Book Title').grid(row=0, column=1)
        self.title_entry = ct.CTkEntry(sub_frame_scan_book1, textvariable=self.title)
        self.title_entry.grid(row=1, column=1, sticky=(tk.W + tk.E), padx=2)

        self.author = tk.StringVar()
        ct.CTkLabel(sub_frame_scan_book1, text='Author').grid(row=0, column=2)
        self.author_entry = ct.CTkEntry(sub_frame_scan_book1, textvariable=self.author)
        self.author_entry.grid(row=1, column=2, sticky=(tk.W + tk.E), padx=2)

        self.cost_price = tk.StringVar()
        ct.CTkLabel(sub_frame_scan_book1, text='Cost Price(IQD)').grid(row=2, column=0)
        self.cost_price_entry = ct.CTkEntry(sub_frame_scan_book1, textvariable=self.cost_price)
        self.cost_price_entry.grid(row=3, column=0, sticky=(tk.W + tk.E), pady=(0, 10), padx=(10, 2))

        self.selling_price = tk.StringVar()
        ct.CTkLabel(sub_frame_scan_book1, text='Selling Price(IQD)').grid(row=2, column=1)
        self.selling_price_entry = ct.CTkEntry(sub_frame_scan_book1, textvariable=self.selling_price)
        self.selling_price_entry.grid(row=3, column=1, sticky=(tk.W + tk.E), pady=(0, 10), padx=2)

        self.qty = tk.StringVar()
        ct.CTkLabel(sub_frame_scan_book1, text='Qty').grid(row=2, column=2)
        self.qty_entry = ct.CTkEntry(sub_frame_scan_book1, textvariable=self.qty)
        self.qty_entry.grid(row=3, column=2, sticky=(tk.W + tk.E), pady=(0, 10), padx=2)

        # Frames for radio buttons
        self.rb_frame = ct.CTkFrame(sub_frame_scan_book1)
        self.rb_frame.rowconfigure(0, weight=1)
        self.rb_frame.columnconfigure(0, weight=1)
        self.rb_frame.grid(row=0, column=3, columnspan=3, rowspan=4, pady=(10, 10), padx=10, sticky='nws')

        self.copy_quality = tk.IntVar()
        self.copy_quality.set(0)
        self.rb_fake_copy = ct.CTkRadioButton(self.rb_frame, text='Fake Copy', variable=self.copy_quality, value=0)
        self.rb_fake_copy.grid(row=0, column=0, sticky='W', padx=10, pady=10)

        self.rb_original_copy = ct.CTkRadioButton(self.rb_frame, text='Original Copy', variable=self.copy_quality,
                                                  value=1)
        self.rb_original_copy.grid(row=1, column=0, sticky='W', padx=10, pady=10)

        self.rb_printed = ct.CTkRadioButton(self.rb_frame, text='Printed', variable=self.copy_quality,
                                            value=2)
        self.rb_printed.grid(row=2, column=0, sticky='W', padx=10, pady=10)

        self.cover = tk.IntVar()
        self.cover.set(0)
        self.rb_cover_paperback = ct.CTkRadioButton(self.rb_frame, text='Paperback', variable=self.cover, value=0)
        self.rb_cover_paperback.grid(row=0, column=1, sticky='W', padx=10, pady=10)
        self.rb_cover_hardcover = ct.CTkRadioButton(self.rb_frame, text='Hardcover', variable=self.cover, value=1)
        self.rb_cover_hardcover.grid(row=1, column=1, sticky='W', padx=10, pady=10)

        self.variables = dict()
        self.variables = {'barcode': self.barcode, 'title': self.title, 'author': self.author,
                          'cost_price': self.cost_price, 'selling_price': self.selling_price, 'qty': self.qty}
        self.rb_variables = dict()
        self.rb_variables = {'Cover': self.cover, 'Copy': self.copy_quality}

        ###################
        # Treeview widget #
        ###################
        self.tree_view = ttk.Treeview(main_frame2, height=20)
        self.tree_view.grid(sticky=(tk.W + tk.E + tk.S + tk.N))

        # Define my columns
        tree_view_columns = ("ID", "Barcode", "Book Title", "Author", "Price", "Qty")
        self.tree_view.configure(columns=tree_view_columns)

        # Format our columns
        self.tree_view.column("ID", anchor=tk.CENTER, width=25)
        self.tree_view.column("Barcode", anchor=tk.CENTER, width=80)
        self.tree_view.column("Book Title", anchor=tk.CENTER, width=150)
        self.tree_view.column("Author", anchor=tk.CENTER, width=150)
        self.tree_view.column("Price", anchor=tk.CENTER, width=25)
        self.tree_view.column("Qty", anchor=tk.CENTER, width=25)

        # Create headings
        for heading in tree_view_columns:
            self.tree_view.heading(heading, text=heading)

        self.tree_view.configure(show='headings')

        # create CTk scrollbar
        ctk_textbox_scrollbar = ct.CTkScrollbar(main_frame2, command=self.tree_view.yview)
        ctk_textbox_scrollbar.grid(row=0, column=0, sticky=(tk.N + tk.S + tk.E))

        # connect textbox scroll event to CTk scrollbar
        self.tree_view.configure(yscrollcommand=ctk_textbox_scrollbar.set)

        # Data entry buttons
        self.add_book_btn = ct.CTkFrame(frame_center, corner_radius=0)
        self.add_book_btn.grid(sticky=(tk.E + tk.W + tk.S + tk.N))
        add_button = ct.CTkButton(self.add_book_btn, text='Add Book', height=40, fg_color='#E74C3C')
        add_button.pack(side=tk.RIGHT, pady=10, padx=(0, 10))

        reset_button = ct.CTkButton(self.add_book_btn, text='Reset', height=40)
        reset_button.pack(side=tk.RIGHT, pady=10, padx=(0, 7))

        # Data entry status bar
        status_variable = tk.StringVar()
        self.status = ct.CTkLabel(
            self.add_book_btn, textvariable=status_variable
        ).pack(side=tk.LEFT, pady=10, padx=10)

        # Data entry functions
        def on_reset():
            """Called when the reset button is clicked"""
            for variable in self.variables.values():
                variable.set('')
            self.barcode_entry.focus()

        reset_button.configure(command=on_reset)
        self.records_saved = 0
                
        def on_save():
            """Save data to the database"""
            # Get current date and time
            self.now = datetime.datetime.today().strftime('%Y-%m-%d')
            data = dict()
            for key, variable in self.variables.items():
                data[key] = variable.get()
            data.update({'cover': self.cover.get(), 'copy': self.copy_quality.get(),
                         'date_added': self.now})

            # Create a tuple from data dictionary
            book_info = (data['barcode'], data['title'].title(), data['author'].title(), data['cost_price'],
                         data['selling_price'], data['qty'], data['cover'], data['copy'], data['date_added'])

            # Insert tuple book_info into the database
            cursor.execute('''INSERT INTO Books (barcode, title, author, cost_price, selling_price, qty, cover, copy, 
            date_added)VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', book_info)
            db.commit()

            self.records_saved += 1
            status_variable.set(f"{self.records_saved} records saved this session")

            # Fetch the most recent entry in the database into treeview
            cursor.execute('SELECT * FROM Books ORDER BY id DESC LIMIT 1')
            data = cursor.fetchall()
            for row in data:
                self.tree_view.insert('', 'end', text='', values=(row[0], row[1], row[2], row[3], row[5], row[6]))

            messagebox.showinfo("Success", "Book added successfully.")
            on_reset()
            self.barcode_entry.focus()

        def check():
            """Data validation and duplicate data check"""
            data = dict()
            required_fields = []
            for key, variable in self.variables.items():
                data[key] = variable.get()
                if data[key] == '':
                    required_fields = required_fields + [key]
            words_string = ", ".join(required_fields)
            if not data['barcode'] or not data['title'] or not data['author'] or not data['selling_price']:
                messagebox.showwarning("Error", f'Please fill in all the required fields: {words_string}')
                return

            cursor.execute('SELECT * FROM Books WHERE barcode = ?', (data['barcode'],))
            result = cursor.fetchone()
            if result:
                user_input = messagebox.askquestion('Oops', '''A record with this barcode already exists. 
                Do you want to update it?''')
                if user_input == 'yes':
                    cursor.execute("UPDATE Books SET title=?, author=?, cost_price=? selling_price? qty?, cover? copy?"
                                   "data_added? WHERE barcode=?",
                                   (data['title'].title(), data['author'].title(), data['cost_price'],
                                    data['selling_price'], data['qty'], data['cover'], data['copy'], data['data_added'],
                                    data['Barcode']))
                    messagebox.showinfo("Success", "Record updated successfully!")
                    db.commit()
                    return
                else:
                    return
            else:
                on_save()

        add_button.configure(command=check)

        def focus_next_widget(event):
            event.widget.tk_focusNext().focus()

        self.barcode_entry.bind("<Return>", focus_next_widget)
        self.title_entry.bind("<Return>", focus_next_widget)
        self.author_entry.bind("<Return>", focus_next_widget)
        self.cost_price_entry.bind("<Return>", focus_next_widget)
        self.selling_price_entry.bind("<Return>", focus_next_widget)
        self.qty_entry.bind("<Return>", focus_next_widget)

