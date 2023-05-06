import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import datetime
import customtkinter as ct
import sqlite3
import csv
import matplotlib.pyplot as plt
import os

with sqlite3.connect("c_bookshop_db.db") as db:
    cursor = db.cursor()


class Reports(ct.CTkFrame):
    def __init__(self, container, controller):
        super().__init__(container)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        ##########
        # Frames #
        ##########
        self.frame_right = ct.CTkFrame(self, fg_color='transparent')
        self.frame_right.grid(row=0, column=0, padx=10, pady=(5, 10), sticky='NW')

        self.frame_generate_reports = ct.CTkFrame(self.frame_right, fg_color='white')
        self.frame_generate_reports.grid(row=0, column=0, pady=5, sticky='NWE')

        self.frame_sales_graph = ct.CTkFrame(self.frame_right, fg_color='white')
        self.frame_sales_graph.grid(row=1, column=0, pady=5, sticky='NWE')

        self.frame_tree_view = ct.CTkFrame(self, fg_color='transparent')
        self.frame_tree_view.grid(row=0, column=1, sticky='news', pady=(0, 10), padx=10)
        self.frame_tree_view.rowconfigure(0, weight=0)
        self.frame_tree_view.rowconfigure(1, weight=1)
        self.frame_tree_view.columnconfigure(0, weight=0)
        self.frame_tree_view.columnconfigure(1, weight=0)
        self.frame_tree_view.columnconfigure(2, weight=0)
        self.frame_tree_view.columnconfigure(3, weight=0)
        self.frame_tree_view.columnconfigure(4, weight=1)

        ###########
        # Widgets #
        ###########
        self.btn_today = ct.CTkButton(self.frame_tree_view, text='Today', height=40, command=self.today)
        self.btn_today.grid(row=0, column=0, sticky='NW', pady=10, padx=(10, 0))

        self.btn_today = ct.CTkButton(self.frame_tree_view, text='This Week', height=40, command=self.week)
        self.btn_today.grid(row=0, column=1, sticky='NW', pady=10, padx=5)

        self.btn_today = ct.CTkButton(self.frame_tree_view, text='This Month', height=40, command=self.month)
        self.btn_today.grid(row=0, column=2, sticky='NW', pady=10, padx=(0, 10))

        # Labels
        self.lbl_generate_reports = ct.CTkLabel(self.frame_generate_reports, text='Sales Report',
                                                font=ct.CTkFont(size=18))
        self.lbl_generate_reports.grid(row=0, column=0, padx=10, pady=10, sticky='NW')

        self.lbl_sale_graphs = ct.CTkLabel(self.frame_sales_graph, text='Sales Graph',
                                           font=ct.CTkFont(size=18))
        self.lbl_sale_graphs.grid(row=0, column=0, padx=10, pady=10, sticky='NW')

        # Buttons
        self.generate_today_sale_csv = ct.CTkButton(self.frame_generate_reports, text="Today CSV",
                                                    command=self.generate_today_csv)
        self.generate_today_sale_csv.grid(row=1, column=0, padx=10, sticky='w', pady=(0, 5))

        self.generate_today_sale_csv = ct.CTkButton(self.frame_generate_reports, text="This Week CSV",
                                                    command=self.generate_week_csv)
        self.generate_today_sale_csv.grid(row=2, column=0, padx=10, sticky='w', pady=(5, 5))

        self.generate_today_sale_csv = ct.CTkButton(self.frame_generate_reports, text="This Month CSV",
                                                    command=self.generate_month_csv)
        self.generate_today_sale_csv.grid(row=3, column=0, padx=10, sticky='w', pady=(5, 10))

        self.btn_daily_sales = ct.CTkButton(self.frame_sales_graph, text="Daily Sales",
                                            )
        self.btn_daily_sales.grid(row=1, column=0, padx=10, pady=(0, 5))

        self.btn_weekly_sales = ct.CTkButton(self.frame_sales_graph, text="Weekly Sales",
                                             )
        self.btn_weekly_sales.grid(row=2, column=0, padx=10, pady=(5, 5))

        self.btn_monthly_sales = ct.CTkButton(self.frame_sales_graph, text="Monthly Sales",
                                              )
        self.btn_monthly_sales.grid(row=3, column=0, padx=10, pady=(5, 10))

        self.total_sales = 0
        self.lbl_total_sales = ct.CTkLabel(self.frame_tree_view, text=f'Total Sales: {self.total_sales}',
                                           font=ct.CTkFont(size=20, weight="bold"), text_color='red')
        self.lbl_total_sales.grid(row=0, column=3, sticky='NWS', pady=10, padx=(10, 10))

        self.total_amount = 0
        self.lbl_total_amount = ct.CTkLabel(self.frame_tree_view, text=f'Total Amount: {self.total_amount} IQD',
                                            font=ct.CTkFont(size=20, weight="bold"), text_color='red')
        self.lbl_total_amount.grid(row=0, column=4, sticky='NWS', pady=10, padx=(10, 10))

        ####################
        # Tree View widget #
        ####################
        self.tree_view = ttk.Treeview(self.frame_tree_view)
        self.tree_view.grid(row=1, column=0, sticky='NEWS', pady=(0, 10), padx=10, columnspan=5)

        # create CTk scrollbar
        ctk_textbox_scrollbar = ct.CTkScrollbar(self.frame_tree_view, command=self.tree_view.yview,
                                                fg_color='transparent')
        ctk_textbox_scrollbar.grid(row=1, column=4, sticky="nse")

        # connect textbox scroll event to CTk scrollbar
        self.tree_view.configure(yscrollcommand=ctk_textbox_scrollbar.set)

        treeview_columns = ('Receipt Number', 'Date', 'Cashier', 'Book', 'Qty', 'Price', 'Total')
        self.tree_view.configure(columns=treeview_columns)

        for heading in treeview_columns:
            self.tree_view.heading(heading, text=heading)

        # Format our columns
        self.tree_view.column("Receipt Number", anchor=tk.CENTER, width=150)
        self.tree_view.column("Date", anchor=tk.CENTER, width=200)
        self.tree_view.column("Cashier", anchor=tk.CENTER, width=100)
        self.tree_view.column("Book", anchor=tk.CENTER, width=200)
        self.tree_view.column("Qty", anchor=tk.CENTER, width=50)
        self.tree_view.column("Price", anchor=tk.CENTER, width=75)
        self.tree_view.column("Total", anchor=tk.CENTER, width=75)

        self.tree_view.configure(show='headings')

    def calculate_totals(self):
        self.total_amount = 0
        self.total_sales = len(self.tree_view.get_children())
        self.lbl_total_sales.configure(text=f'Total Sales: {self.total_sales}')

        if self.tree_view.get_children():
            for item in self.tree_view.get_children():
                value = self.tree_view.item(item)['values'][6]
                self.total_amount += float(value)

        self.lbl_total_amount.configure(text=f'Total Amount: {self.total_amount} IQD')

    @staticmethod
    def date(self, period):
        """Calculate date period."""
        period_output = 0
        if period == 0:
            # Select all records from the Sales table that were added today
            period_output = datetime.date.today()
        elif period == 1:
            # Get today's date
            today = datetime.date.today()

            # Calculate the number of days since the start of the week (Saturday = 6)
            days_since_start_of_week = (today.weekday() - 5) % 7

            # Calculate the start and end dates of the week
            start_of_week = today - datetime.timedelta(days=days_since_start_of_week)
            end_of_week = start_of_week + datetime.timedelta(days=6)
            period_output = (start_of_week, end_of_week)
        elif period == 2:
            # Get the current month as a two-digit string with leading zeros
            current_month = datetime.datetime.now().strftime('%m')
            period_output = current_month
        return period_output

    def today(self):
        """ List all today's sold items. """
        self.clear_tree_view()
        query = "SELECT * FROM Sales WHERE DATE(date) = DATE(?)"
        cursor.execute(query, (self.date(self, 0),))
        sales = cursor.fetchall()
        for sale in sales:
            self.tree_view.insert('', 'end', text='', values=(sale[0], sale[1], sale[2], sale[3], sale[4], sale[5],
                                                              sale[6]))

        self.calculate_totals()

    def week(self):
        self.clear_tree_view()

        # Execute the query to select the sales entries for the current week
        query = "SELECT * FROM Sales WHERE Date BETWEEN ? AND ?"
        cursor.execute(query, self.date(self, 1))
        sales = cursor.fetchall()
        for sale in sales:
            self.tree_view.insert('', 'end', text='', values=(sale[0], sale[1], sale[2], sale[3], sale[4], sale[5],
                                                              sale[6]))
        self.calculate_totals()

    def month(self):
        self.clear_tree_view()

        cursor.execute("SELECT * FROM Sales WHERE strftime('%m', date) = ?", (self.date(self, 2),))
        sales = cursor.fetchall()
        for sale in sales:
            self.tree_view.insert('', 'end', text='', values=(sale[0], sale[1], sale[2], sale[3], sale[4], sale[5],
                                                              sale[6]))

        self.calculate_totals()

    def clear_tree_view(self):
        children = self.tree_view.get_children()
        if children:
            self.tree_view.delete(*children)

    def generate_today_csv(self):

        # Get the absolute path to the desktop directory
        desktop_dir = os.path.join(os.path.expanduser("~"), "Desktop")

        # Define the CSV file name and location
        csv_file = f'{desktop_dir}\\sales_today.csv'

        query = "SELECT * FROM Sales WHERE DATE(date) = DATE(?)"
        cursor.execute(query, (self.date(self, 0),))
        sales = cursor.fetchall()

        # Open the CSV file in write mode
        with open(csv_file, 'w', newline='') as file:
            # Create a CSV writer object
            writer = csv.writer(file)

            # Write the header row
            writer.writerow(['Receipt Number', 'Date', 'Cashier', 'Book', 'Qty', 'Price', 'Total'])

            # Iterate over the rows and write them to the CSV file
            for sale in sales:
                writer.writerow(sale)

        # Close the CSV file
        file.close()

        # Messagebox
        messagebox.showinfo("Success", "CSV Report generated successfully!")

    def generate_week_csv(self):
        """ Generate CSV file for all items sold in current week. """
        # Get the absolute path to the desktop directory
        desktop_dir = os.path.join(os.path.expanduser("~"), "Desktop")

        # Define the CSV file name and location
        csv_file = f'{desktop_dir}\\sales_current_week.csv'

        # Execute the query to select the sales entries for the current week
        query = "SELECT * FROM Sales WHERE Date BETWEEN ? AND ?"
        cursor.execute(query, self.date(self, 1))
        sales = cursor.fetchall()

        # Open the CSV file in write mode
        with open(csv_file, 'w', newline='') as file:
            # Create a CSV writer object
            writer = csv.writer(file)

            # Write the header row
            writer.writerow(['Receipt Number', 'Date', 'Cashier', 'Book', 'Qty', 'Price', 'Total'])

            # Iterate over the rows and write them to the CSV file
            for sale in sales:
                writer.writerow(sale)

        # Close the CSV file
        file.close()

        # Messagebox
        messagebox.showinfo("Success", "CSV Report generated successfully!")

    def generate_month_csv(self):
        # Get the absolute path to the desktop directory
        desktop_dir = os.path.join(os.path.expanduser("~"), "Desktop")

        # Define the CSV file name and location
        csv_file = f'{desktop_dir}\\sales_current_month.csv'

        # Execute the query and fetch the results
        cursor.execute("SELECT * FROM Sales WHERE strftime('%m', date) = ?", (self.date(self, 2),))
        sales = cursor.fetchall()

        # Open the CSV file in write mode
        with open(csv_file, 'w', newline='') as file:
            # Create a CSV writer object
            writer = csv.writer(file)

            # Write the header row
            writer.writerow(['Receipt Number', 'Date', 'Cashier', 'Book', 'Qty', 'Price', 'Total'])

            # Iterate over the rows and write them to the CSV file
            for sale in sales:
                writer.writerow(sale)

        # Close the CSV file
        file.close()

        # Messagebox
        messagebox.showinfo("Success", "CSV Report generated successfully!")



