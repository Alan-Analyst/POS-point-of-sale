import tkinter as tk
from tkinter import ttk
import customtkinter as ct
import sqlite3
from playsound import playsound
from datetime import datetime
from tkinter import messagebox
import win32print
import configparser

with sqlite3.connect("c_bookshop_db.db") as db:
    cursor = db.cursor()


class Pos(ct.CTkFrame):
    def __init__(self, container, controller):
        super().__init__(container)
        ##########
        # Frames #
        ###########
        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)

        self.parent_frame = ct.CTkFrame(self)
        self.parent_frame.grid(row=0, column=0, sticky='NEWS')
        self.parent_frame.columnconfigure(0, weight=0)
        self.parent_frame.columnconfigure(1, weight=3)
        self.parent_frame.rowconfigure(0, weight=1)

        # Left frame a
        self.frame_left_a = ct.CTkFrame(self.parent_frame, corner_radius=0, fg_color='transparent')
        self.frame_left_a.grid(row=0, column=0, sticky='NEWS', padx=10, pady=10)
        self.frame_left_a.rowconfigure(0, weight=1)
        self.frame_left_a.columnconfigure(0, weight=1)

        # Left frame child
        self.frame_left_child = ct.CTkFrame(self.frame_left_a, corner_radius=0)
        self.frame_left_child.grid(row=0, column=0, sticky='NEWS')
        for i in range(9):
            self.frame_left_child.columnconfigure(i, weight=1)
        for i in range(9):
            self.frame_left_child.rowconfigure(i, weight=0)
        self.frame_left_child.rowconfigure(99, weight=1)

        # Right Frame a
        self.frame_right_a = ct.CTkFrame(self.parent_frame, corner_radius=0, fg_color='transparent')
        self.frame_right_a.grid(row=0, column=1, sticky='NEWS', pady=10, padx=10)
        self.frame_right_a.rowconfigure(0, weight=1)
        self.frame_right_a.columnconfigure(0, weight=1)

        # Left frame widgets
        # Font Label
        self.lbl_price = ct.CTkLabel(self.frame_left_child, text='', font=ct.CTkFont(size=24, weight="bold"),
                                     height=70, fg_color=("black", "white"), text_color=('red', 'black'))
        self.lbl_price.grid(row=0, column=0, sticky='WEN', columnspan=3)

        # Scan barcode label and entry box
        self.lbl = ct.CTkLabel(self.frame_left_child, text='Scan Barcode:',
                               font=ct.CTkFont(size=24, weight="bold")).grid(row=1, column=0, sticky='E', padx=(0, 5),
                                                                             pady=(20, 5))
        self.scan = tk.StringVar()
        self.ent_scan = ct.CTkEntry(self.frame_left_child, corner_radius=0, textvariable=self.scan,
                                    font=('Calibri', 24, 'bold'))
        self.ent_scan.grid(row=1, column=1, pady=(20, 5), sticky='WE', columnspan=2)
        self.ent_scan.focus()

        # Quantity label and button
        self.lbl = ct.CTkLabel(self.frame_left_child, text='Qty:',
                               font=ct.CTkFont(size=20, weight="bold")).grid(row=2, column=0, sticky='E', padx=(0, 5),
                                                                             pady=(5, 5))
        self.lbl_qty = ct.CTkLabel(self.frame_left_child, text='',
                                   fg_color="black", text_color='red',
                                   font=ct.CTkFont(size=20, weight="bold"),
                                   )
        self.lbl_qty.grid(row=2, column=1, sticky='WE', padx=(0, 5), pady=(5, 5))

        self.btn_qty = ct.CTkButton(self.frame_left_child,
                                    text='Change Quantity', command=self.change_qty)
        self.btn_qty.grid(row=2, column=2, pady=(5, 5), sticky='W')

        self.lbl = ct.CTkLabel(self.frame_left_child, text='Subtotal:',
                               font=ct.CTkFont(size=20, weight="bold")).grid(row=3, column=0, sticky='E', padx=(0, 5),
                                                                             pady=(5, 5))
        self.lbl_subtotal = ct.CTkLabel(self.frame_left_child, text='',
                                        fg_color="black", text_color='red',
                                        font=ct.CTkFont(size=20, weight="bold"), width=150
                                        )
        self.lbl_subtotal.grid(row=3, column=1, sticky='WE', padx=(0, 5), pady=(5, 5))

        self.lbl = ct.CTkLabel(self.frame_left_child, text='Discount(%):',
                               font=ct.CTkFont(size=20, weight="bold")).grid(row=4, column=0, sticky='E', padx=(0, 5),
                                                                             pady=(5, 5))
        self.lbl_discount = ct.CTkLabel(self.frame_left_child, text='',
                                        fg_color="black", text_color='red',
                                        font=ct.CTkFont(size=20, weight="bold"), width=150
                                        )
        self.lbl_discount.grid(row=4, column=1, sticky='WE', padx=(0, 5), pady=(5, 5))

        self.btn_discount = ct.CTkButton(self.frame_left_child,
                                         text='Apply Discount', command=self.apply_discount)
        self.btn_discount.grid(row=4, column=2, pady=(5, 5), sticky='W')

        self.lbl = ct.CTkLabel(self.frame_left_child, text='Payment(Cash):',
                               font=ct.CTkFont(size=20, weight="bold")).grid(row=5, column=0, sticky='E', padx=(0, 5),
                                                                             pady=(5, 5))
        self.lbl_payment = ct.CTkLabel(self.frame_left_child, text='',
                                       fg_color="black", text_color='red',
                                       font=ct.CTkFont(size=20, weight="bold"), width=150
                                       )
        self.lbl_payment.grid(row=5, column=1, sticky='WE', padx=(0, 5), pady=(5, 5))

        self.btn_payment = ct.CTkButton(self.frame_left_child,
                                        text='Payment', command=self.get_payment)
        self.btn_payment.grid(row=5, column=2, pady=(5, 5), sticky='W')

        self.lbl = ct.CTkLabel(self.frame_left_child, text='Change Back:',
                               font=ct.CTkFont(size=20, weight="bold")).grid(row=6, column=0, sticky='E', padx=(0, 5),
                                                                             pady=(5, 5))
        self.lbl_change = ct.CTkLabel(self.frame_left_child, text='',
                                      fg_color="black", text_color='red',
                                      font=ct.CTkFont(size=20, weight="bold"), width=150
                                      )
        self.lbl_change.grid(row=6, column=1, sticky='WE', padx=(0, 5), pady=(5, 5))

        # Buttons
        self.btn_clear = ct.CTkButton(self.frame_left_child, text='Clear', height=40, command=self.ask_before_clear)
        self.btn_clear.grid(row=7, column=1, sticky='E', pady=(20, 5), padx=5)

        self.btn_delete = ct.CTkButton(self.frame_left_child,
                                       text='Delete Row', height=40,
                                       command=self.delete_selected_row_from_tree_view)
        self.btn_delete.grid(row=8, column=1, sticky='E', padx=5)

        self.btn_next = ct.CTkButton(self.frame_left_child, text='Next Customer', height=40,
                                     command=self.next_customer)
        self.btn_next.grid(row=7, column=2, pady=(20, 5), sticky='W')

        self.btn_print = ct.CTkButton(self.frame_left_child, text='Print Receipt', height=40,
                                      command=self.print_receipt, fg_color='#E74C3C', text_color='black')
        self.btn_print.grid(row=8, column=2, sticky='W')

        # Information
        with open('settings.ini', 'r') as f:
            self.cashier_name = f.read()

        # Read the settings file
        config = configparser.ConfigParser()
        config.read('settings.ini')

        # Get the values
        self.cashier_name = config.get('info', 'cashier')
        self.shop_name = config.get('info', 'shop')
        self.address = config.get('info', 'address')
        self.phone = config.get('info', 'phone')

        self.lbl_cashier = ct.CTkLabel(self.frame_left_child, text=f'Cashier: {self.cashier_name}',
                                       font=ct.CTkFont(size=16, weight="bold"), text_color='red')
        self.lbl_cashier.grid(row=9, column=0, columnspan=3, sticky='WS')

        self.lbl_shop = ct.CTkLabel(self.frame_left_child, text=f'Shop: {self.shop_name}',
                                    font=ct.CTkFont(size=16, weight="bold"), text_color='red')
        self.lbl_shop.grid(row=10, column=0, columnspan=3, sticky='WS')

        self.lbl_address = ct.CTkLabel(self.frame_left_child, text=f'Address: {self.address}',
                                       font=ct.CTkFont(size=16, weight="bold"), text_color='red')
        self.lbl_address.grid(row=11, column=0, columnspan=3, sticky='WS')

        self.lbl_phone = ct.CTkLabel(self.frame_left_child, text=f'Bookstore: {self.phone}',
                                     font=ct.CTkFont(size=16, weight="bold"), text_color='red')
        self.lbl_phone.grid(row=12, column=0, columnspan=3, sticky='WS')

        default_printer_name = win32print.GetDefaultPrinter()
        self.cashier_lbl = ct.CTkLabel(self.frame_left_child, text=f'Default Printer: {default_printer_name}',
                                       font=ct.CTkFont(size=16, weight="bold"), text_color='red')
        self.cashier_lbl.grid(row=13, column=0, columnspan=3, sticky='WS')

        self.status_bar = ct.CTkLabel(self.frame_left_child, text='', font=ct.CTkFont(size=14, weight="bold"))
        self.status_bar.grid(row=99, column=0, columnspan=1, sticky='EWS')

        # right frame widgets

        ###################
        # Treeview widget #
        ###################
        self.tree_view = ttk.Treeview(self.frame_right_a)
        self.tree_view.grid(sticky=(tk.W + tk.E + tk.S + tk.N))
        style = ttk.Style()
        style.configure("Treeview", font=18)
        style.configure("Treeview.Heading", font=24)

        # create CTk scrollbar
        ctk_textbox_scrollbar = ct.CTkScrollbar(self.frame_right_a, command=self.tree_view.yview,
                                                fg_color='transparent')
        ctk_textbox_scrollbar.grid(row=0, column=0, sticky="nse")

        # connect textbox scroll event to CTk scrollbar
        self.tree_view.configure(yscrollcommand=ctk_textbox_scrollbar.set)

        treeview_columns = ('ID', 'Book', 'Price(IQD)', 'Qty', 'Total(IQD)')
        self.tree_view.configure(columns=treeview_columns)

        for heading in treeview_columns:
            self.tree_view.heading(heading, text=heading)

        # Format our columns
        self.tree_view.column("ID", anchor=tk.CENTER, width=0)
        self.tree_view.column("Book", anchor=tk.CENTER, width=200)
        self.tree_view.column("Price(IQD)", anchor=tk.CENTER, width=75)
        self.tree_view.column("Qty", anchor=tk.CENTER, width=50)
        self.tree_view.column("Total(IQD)", anchor=tk.CENTER, width=75)

        self.tree_view.configure(show='headings')

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 20))
        style.configure("Treeview", rowheight=35)
        # configure the font size for rows
        style.configure("Treeview", font=("Arial", 20))

        ######################
        # Set default values #
        ######################
        self.subtotal_price, self.discount, self.total_price = float(0), float(0), float(0)
        self.change, self.payment = float(0), float(0)
        self.qty = int(1)
        self.data = tuple()
        self.btn_print.configure(state='disabled')
        self.btn_next.configure(state='disabled')
        self.btn_payment.configure(state='disabled')

        ############
        # Bindings #
        ############
        self.ent_scan.bind('<Return>', self.populate_treeview)
        self.tree_view.bind("<<TreeviewSelect>>", self.on_select_qty_update)

        #################
        # Class methods #
        #################
    def delete_selected_row_from_tree_view(self):
        selection = self.tree_view.selection()
        if selection:
            self.tree_view.delete(*selection)
            self.lbl_qty.configure(text='')
            self.calculate_subtotal()
            self.calculate_total()
            self.calculate_change()
        else:
            pass

    def ask_before_clear(self):
        choice = messagebox.askyesno('Clear?',
                                     '''Receipt information will not be saved in the database. 
Do you still want to proceed?''')

        if choice:
            self.clear_tree_view()
        else:
            pass

    def clear_tree_view(self):
        children = self.tree_view.get_children()
        if children:
            self.tree_view.delete(*children)
            self.calculate_subtotal()
            self.calculate_total()
        self.lbl_change.configure(text='')
        self.lbl_qty.configure(text='')
        self.lbl_price.configure(text='')
        self.lbl_payment.configure(text='')
        self.lbl_discount.configure(text='')
        self.discount, self.payment, self.change = 0, 0, 0
        self.btn_print.configure(state='disabled')
        self.btn_next.configure(state='disabled')
        self.btn_payment.configure(state='disabled')

    def calculate_subtotal(self):
        self.subtotal_price = float(0)
        if self.tree_view.get_children():
            for item in self.tree_view.get_children():
                value = self.tree_view.item(item)['values'][2]
                qty = self.tree_view.item(item)['values'][3]
                value_times_qty = float(value) * int(qty)
                self.tree_view.set(item, 'Total(IQD)', value_times_qty)
                self.subtotal_price += float(value_times_qty)
            self.lbl_subtotal.configure(text=f'{str(self.subtotal_price)}  IQD')
            self.subtotal_price = round(self.subtotal_price, 2)
        else:
            self.lbl_subtotal.configure(text=f'')
        return self.subtotal_price

    def calculate_total(self):
        """Calculate Total Price"""
        self.total_price = self.subtotal_price - (self.discount / 100) * self.subtotal_price
        self.lbl_price.configure(text=self.total_price)
        self.total_price = round(self.total_price, 2)
        return self.total_price

    def change_qty(self):
        """Get qty value from using dialog widget"""
        dialog = ct.CTkInputDialog(text="Type in the quantity:", title="Change Quantity")
        try:
            self.qty = int(dialog.get_input())
        except ValueError:
            pass
        # Call calculate_with_qty function to calculate the total price
        self.calculate_with_qty(self.qty)
        self.lbl_qty.configure(text=self.qty)

    def calculate_with_qty(self, qty):
        selection = self.tree_view.selection()
        if selection:
            item = selection[0]
            if qty == '':
                qty = 1
            self.tree_view.set(item, column='Qty', value=str(qty))
            self.calculate_subtotal()
            self.calculate_total()
            self.calculate_change()
        else:
            return

    def populate_treeview(self, event):
        scan_formatted = self.scan.get()
        scan_formatted.strip()
        cursor.execute('SELECT id, title, selling_price FROM Books WHERE barcode=?',
                       (scan_formatted,))
        result = cursor.fetchone()
        if result:
            if self.check_barcode_exists(result):
                self.not_exit_sound()
            else:
                qty = 1
                self.tree_view.insert('', 'end', text='',
                                      values=(result[0], result[1], result[2], qty,
                                              int(qty) * result[2]))
                self.ent_scan.delete('0', tk.END)
                self.calculate_subtotal()
                self.calculate_total()
                self.btn_payment.configure(state='normal')
        else:
            self.not_exit_sound()
            self.btn_print.configure(state='disabled')

    def get_payment(self):
        dialog = ct.CTkInputDialog(text="Type in the payment:", title="Payment")
        try:
            self.payment = float(dialog.get_input())
        except ValueError:
            pass
        if self.payment:
            self.calculate_change()
        self.btn_print.configure(state='normal')
        self.btn_next.configure(state='normal')

    def calculate_change(self):

        self.change = float(self.payment) - self.calculate_total()
        self.lbl_payment.configure(text=str(self.payment))
        self.lbl_change.configure(text=str(round(self.change, 2)))
        self.change = round(self.change, 2)
        return self.change

    def check_barcode_exists(self, book_id):
        """
        Check if a barcode exists in the specified self.Item treeview widget.

        Args:
            book_id (tuple): The id to search for.
            tree view (ttk.TreeView): The TreeView widget to search in.

        Returns:
            bool: True if the barcode exists in the TreeView, False otherwise.
     """
        for item in self.tree_view.get_children():
            if int(self.tree_view.item(item, 'values')[0]) == book_id[0]:
                return True
        return False

    def apply_discount(self):
        dialog = ct.CTkInputDialog(text="Apply discount in percent:", title="Discount")
        try:
            self.discount = float(dialog.get_input())
            self.lbl_discount.configure(text=f'{self.discount} %')
            self.calculate_total()
            self.calculate_change()
        except ValueError:
            pass

    def on_select_qty_update(self, event):
        try:
            item = event.widget.selection()[0]
            quantity = event.widget.item(item)['values'][3]
            self.lbl_qty.configure(text=quantity)
        except IndexError:
            pass

    def next_customer(self):
        """Insert receipt data into the database Sales table"""
        self.data = tuple()
        if len(self.tree_view.get_children()) != 0:
            now = datetime.now()
            datetime_now = now.strftime("%Y-%m-%d %H:%M")

            # Get the values for the first row of the Treeview
            items = self.tree_view.get_children()

            # Get receipt number
            receipt_number = self.get_receipt_number()

            # Iterate through the items and get their values
            for item in items:
                values = self.tree_view.item(item)['values']
                self.data = (receipt_number, datetime_now, self.cashier_name, values[1], values[3], values[2],
                             values[4])
                # Insert tuple book_info into the database
                cursor.execute('''INSERT INTO Sales (receipt_number, date, cashier, book, qty, price, 
                                          total)VALUES (?, ?, ?, ?, ?, ?, ?)''', self.data)
                db.commit()

            self.clear_tree_view()

    def print_receipt(self):
        """Handle printing the receipt"""
        if len(self.tree_view.get_children()) != 0:

            printer_name = win32print.GetDefaultPrinter()
            self.status_bar.configure(text=printer_name)

            #####################
            # Sale receipt info #
            #####################

            # Define the receipt data
            receipt_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Define the receipt text
            receipt_text = f"""{self.shop_name}\n{self.address}\nPhone: {self.phone}\nDatetime: {receipt_date}
Cashier: {self.cashier_name}\nReceipt #: {self.get_receipt_number()}
{'=' * 45}
Title                          Qty  Price
{'-' * 45}
"""

            # Get the values for the first row of the Treeview
            items = self.tree_view.get_children()

            # Iterate through the items and get their values
            for item in items:
                values = self.tree_view.item(item)['values']

                length = len(values[1][:25])

                if length == 25:
                    length = 6
                elif length <= 25:
                    length = 25 - len(values[1][:25])
                    length += 6

                if len(str(values[3])) == 1:
                    receipt_text += f'{values[1][:25]}{" " * length}{values[3]}{" " * 4}{float(values[4]):6.3f} IQD\n'
                elif len(str(values[3])) == 2:
                    receipt_text += f'{values[1][:25]}{" " * length}{values[3]}{" " * 3}{float(values[4]):6.3f} IQD\n'
                else:
                    receipt_text += f'{values[1][:25]}{" " * length}{values[3]}{" " * 2}{float(values[4]):6.3f} IQD\n'
            receipt_text += f"""{'-' * 45}
Subtotal:{' ' * 25}{self.subtotal_price:6.3f}IQD
Discount:{' ' * 25}{self.discount:6.3f}%
Total:{' ' * 28}{self.total_price:6.3f}IQD
Payment:{' ' * 26}{self.payment:6.3f}IQD
Change:{' ' * 27}{self.change:6.3f}IQD
{'=' * 45}
Thank you for your purchase!
"""
            raw_data = f'b"\x1B\x40{receipt_text}\n\x1D\x56\x41\x10"'

            # Convert the raw data to bytes
            raw_data_bytes = bytes(raw_data, encoding="utf-8")

            # Open printer and print data
            h_printer = win32print.OpenPrinter(printer_name)
            try:
                # Start a new print job
                job_name = "Sale Receipt"
                h_job = win32print.StartDocPrinter(h_printer, 1, (job_name, None, "RAW"))

                # Send the data to the printer
                win32print.StartPagePrinter(h_printer)
                win32print.WritePrinter(h_printer, raw_data_bytes)
                win32print.EndPagePrinter(h_printer)

            finally:
                # Close the printer
                win32print.EndDocPrinter(h_printer)
                win32print.ClosePrinter(h_printer)

    @staticmethod
    def get_receipt_number():
        # Execute the query to check if the first row, first column of the sales table with ID 0 is null or not
        cursor.execute("SELECT * FROM Sales LIMIT 1")
        result = cursor.fetchone()

        # Check the value of the result
        if result:
            cursor.execute("SELECT * FROM Sales ORDER BY rowid DESC LIMIT 1")
            result = cursor.fetchone()
            receipt_number = result[0] + 1

        else:
            receipt_number = 1000

        return receipt_number

    @staticmethod
    def not_exit_sound():
        # Path to sound file
        sound_file_path = 'sound/beep-beep-6151.mp3'
        playsound(sound_file_path)
