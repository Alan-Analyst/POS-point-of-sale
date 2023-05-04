import tkinter as tk
import sqlite3
import customtkinter as ct

with sqlite3.connect("c_bookshop_db.db") as db:
    cursor = db.cursor()


class ItemList(ct.CTkFrame):
    def __init__(self, container, controller):
        super().__init__(container)

        self.barcode = tk.StringVar()
        self.title = tk.StringVar()
        self.author = tk.StringVar()
        self.price = tk.StringVar()

        ##########
        # Frames #
        ##########
        # Parent main frame
        self.grid(row=0, column=0, sticky='news')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)

        # Child top frame
        self.frame_child_top = ct.CTkFrame(self, corner_radius=0)
        self.frame_child_top.grid(row=0, column=0, sticky='news')
        self.frame_child_top.rowconfigure(0, weight=0)

        # Child bottom frame
        self.frame_child_bottom = ct.CTkFrame(self, corner_radius=0)
        self.frame_child_bottom.grid(row=1, column=0, sticky='news')
        self.frame_child_bottom.rowconfigure(0, weight=1)
        self.frame_child_bottom.columnconfigure(0, weight=1)
        self.frame_child_bottom.columnconfigure(1, weight=1)

        # Grand child search frame
        self.frame_grandchild_search_frame = ct.CTkFrame(self.frame_child_top, fg_color='transparent')
        self.frame_grandchild_search_frame.grid(row=0, column=0, sticky='NSW')
        for i in range(4):
            self.frame_grandchild_search_frame.columnconfigure(i, weight=1)

        # Grand child buttons frame
        self.frame_grandchild_buttons = ct.CTkFrame(self.frame_child_top, fg_color='transparent')
        self.frame_grandchild_buttons.grid(row=0, column=1, sticky='NSW')
        self.frame_grandchild_buttons.rowconfigure(0, weight=1)

        # Grand child statistics frame
        self.frame_grandchild_statistics = ct.CTkFrame(self.frame_child_top, fg_color='transparent')
        self.frame_grandchild_statistics.grid(row=0, column=2, sticky='NSW')
        self.frame_grandchild_statistics.rowconfigure(0, weight=1)

        ###########
        # Widgets #
        ###########
        # Search label
        lbl_search = ct.CTkLabel(self.frame_grandchild_search_frame, text='Search:')
        lbl_search.grid(row=0, column=0, padx=(10, 4), pady=10, sticky='WE')

        # Search entry
        self.search_var = tk.StringVar()
        self.ent_search = ct.CTkEntry(self.frame_grandchild_search_frame, textvariable=self.search_var, width=260)
        self.ent_search.grid(row=0, column=1, columnspan=3, pady=10, sticky='W')
        # search by, radio buttons
        self.search_by = tk.IntVar()
        self.rb_title = ct.CTkRadioButton(self.frame_grandchild_search_frame, text='Title', variable=self.search_by,
                                          value=0, command=lambda: self.display(self, search_by=0))
        self.rb_author = ct.CTkRadioButton(self.frame_grandchild_search_frame, text='Author', variable=self.search_by,
                                           value=1, command=lambda: self.display(self, search_by=1))
        self.rb_isbn = ct.CTkRadioButton(self.frame_grandchild_search_frame, text='ISBN', variable=self.search_by,
                                         value=2, command=lambda: self.display(self, search_by=2))

        self.rb_title.grid(row=1, column=1, pady=(0, 10), sticky='WE')
        self.rb_author.grid(row=1, column=2, pady=(0, 10), sticky='WE')
        self.rb_isbn.grid(row=1, column=3, pady=(0, 10), sticky='WE')

        self.view_all = ct.CTkButton(self.frame_grandchild_buttons, text='View All', height=40,
                                     command=lambda: self.display(self, search_by=0))
        self.view_all.grid(row=0, column=0, pady=10, padx=(0, 5))
        self.button_update_selected = ct.CTkButton(self.frame_grandchild_buttons, text='Update Selected', height=40)
        self.button_update_selected.grid(row=0, column=1, pady=10, padx=(5, 5))
        self.button_delete_selected = ct.CTkButton(self.frame_grandchild_buttons, text='Delete Selected', height=40)
        self.button_delete_selected.grid(row=0, column=2, pady=10, padx=(5, 0))

        self.list_book = tk.Listbox(self.frame_child_bottom, bd=6,  font='Calibri 18 bold')
        self.list_book.grid(row=0, column=0, padx=(10, 23), sticky='NEWS')

        # create CTk scrollbar
        ctk_textbox_scrollbar_v = ct.CTkScrollbar(self.frame_child_bottom, command=self.list_book.yview,
                                                  fg_color='transparent')
        ctk_textbox_scrollbar_v.grid(row=0, column=0, sticky="nse")

        # connect textbox scroll event to CTk scrollbar
        self.list_book.configure(yscrollcommand=ctk_textbox_scrollbar_v.set)

        # List details
        self.list_details = tk.Listbox(self.frame_child_bottom, bd=6, font='Calibri 18 bold')
        self.list_details.grid(row=0, column=1, padx=(10, 0), sticky='NEWS')

        # Statistics
        self.lbl_book_count = ct.CTkLabel(self.frame_grandchild_statistics, text='', padx=20, text_color="red",
                                          font=('verdana', 16, 'bold'))
        self.lbl_book_count.grid(row=0, column=0)

        ###############
        # Event binds #
        ###############
        self.list_book.bind('<<ListboxSelect>>', self.display_book_info)
        self.ent_search.bind('<KeyRelease>', self.search_book_by)

        #################
        # Class methods #
        #################
    def display_books(self, event, search_by):
        if search_by == 0:
            self.list_book.delete('0', tk.END)
            books = cursor.execute('SELECT id, title FROM Books').fetchall()
            count = 0
            for book in books:
                self.list_book.insert(count, str(book[0]) + '- ' + book[1])
                count += 1
        elif search_by == 1:
            self.list_book.delete('0', tk.END)
            books = cursor.execute('SELECT id, author FROM Books').fetchall()
            count = 0
            for book in books:
                self.list_book.insert(count, str(book[0]) + '- ' + book[1])
                count += 1
        elif search_by == 2:
            self.list_book.delete('0', tk.END)
            books = cursor.execute('SELECT id, barcode FROM Books').fetchall()
            count = 0
            for book in books:
                self.list_book.insert(count, str(book[0]) + '- ' + str(book[1]))
                count += 1

    def display_book_info(self, event):
        value = str(self.list_book.get(tk.ACTIVE))
        book_id = value.split('-')[0]
        my_book = cursor.execute('SELECT * FROM Books WHERE id=?', (book_id,))
        book_info = my_book.fetchall()
        self.list_details.delete(0, tk.END)
        # Fix this error
        self.list_details.insert(0, f'ISBN: {book_info[0][1]}')
        # Copy ISBN to clip board when a book is selected
        self.clipboard_clear()
        self.clipboard_append(book_info[0][1])
        self.list_details.insert(1, f'Book Title: {book_info[0][2]}')
        self.list_details.insert(2, f'Author: {book_info[0][3]}')
        self.list_details.insert(3, f'Cost Price(IQD):  {book_info[0][4]}')
        self.list_details.insert(4, f'Selling Price(IQD): {book_info[0][5]}')
        if book_info[0][6] == 0:
            self.list_details.insert(5, 'Qty: Not available, please order as soon as possible!')
        else:
            self.list_details.insert(5, f'Qty: {book_info[0][5]}')
        if book_info[0][7] == 0:
            self.list_details.insert(6, 'Paperback')
        else:
            self.list_details.insert(6, 'Hardcover')
        if book_info[0][8] == 0:
            self.list_details.insert(7, 'Fake Copy')
        elif book_info[0][8] == 1:
            self.list_details.insert(7, 'Original Copy')
        else:
            self.list_details.insert(7, 'Printed')
        self.list_details.insert(8, f'Date Added: {book_info[0][9]}')
        self.list_details.insert(9, f'Category: {book_info[0][10]}')

    def display(self, event, search_by):
        self.display_books(event, search_by)
        self.display_statistics(event)

    # Search Function
    def search_book_by(self, event):
        # Grab what was typed
        typed = self.search_var.get()
        if typed == '' or typed.strip() == '':
            self.list_book.delete('0', tk.END)
            self.display_books(self, self.search_by.get())
        else:
            if self.search_by.get() == 0:
                search = cursor.execute("SELECT id, title FROM Books WHERE title LIKE ?",
                                        ('%' + typed + '%',)).fetchall()
                self.list_book.delete(0, tk.END)
                count = 0
                for book in search:
                    self.list_book.insert(count, str(book[0]) + "- " + book[1])
                    count += 1
            elif self.search_by.get() == 1:
                search = cursor.execute("SELECT id, author FROM Books WHERE author LIKE ?",
                                        ('%' + typed + '%',)).fetchall()
                self.list_book.delete(0, tk.END)
                count = 0
                for book in search:
                    self.list_book.insert(count, str(book[0]) + "- " + book[1])
                    count += 1
            elif self.search_by.get() == 2:
                search = cursor.execute("SELECT id, barcode FROM Books WHERE barcode LIKE ?",
                                        ('%' + typed + '%',)).fetchall()
                self.list_book.delete(0, tk.END)
                count = 0
                for book in search:
                    self.list_book.insert(count, str(book[0]) + "- " + str(book[1]))
                    count += 1

    def display_statistics(self, event):
        count_books = cursor.execute("SELECT count(id) FROM books").fetchall()
        self.lbl_book_count.configure(text='Total: ' + str(count_books[0][0]) + ' books in the database')
