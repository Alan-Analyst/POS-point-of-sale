import tkinter as tk
# from tkinter import ttk
btn_background = '#fcc324'
test_background = '#9bc9ff'


class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('Cambridge Bookshop Point of Sale 2023')
        self.geometry('1350x750+300+100')
        self.minsize(783, 500)
        self.iconbitmap('images/icon.ico')
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Main frame
        self.frame = tk.Frame(self)
        self.frame.grid(sticky=(tk.E + tk.W + tk.S + tk.N))
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=0)
        self.frame.rowconfigure(1, weight=120)

        # Top frame
        self.frame_top = tk.Frame(self.frame, bg=test_background, relief='sunken', borderwidth=2)
        self.frame_top.grid(row=0, column=0, sticky='new')

        # Center frame
        self.frame_center = tk.Frame(self.frame, relief='ridge', bg='#e0f0f0', borderwidth=2)
        self.frame_center.grid(row=1, column=0, sticky='news')
        self.frame_center.columnconfigure(0, weight=1)
        self.frame_center.columnconfigure(1, weight=0)
        self.frame_center.rowconfigure(0, weight=1)

        # Toolbox buttons
        self.image_make_a_sale = tk.PhotoImage(file='images/point-of-sale.png')
        self.btn_make_a_sale = tk.Button(self.frame_top, image=self.image_make_a_sale, compound='left',
                                         text='Make a Sale', font=('arial', 12, 'bold'), height=50, bg=btn_background)
        self.btn_make_a_sale.grid(row=0, column=0, padx=0, pady=0, ipady=3, ipadx=5)

        self.image_item_list = tk.PhotoImage(file='images/database.png')
        self.btn_item_list = tk.Button(self.frame_top, text='Item List', font=('arial', 12, 'bold'),
                                       image=self.image_item_list, compound='left', height=50, bg=btn_background)
        self.btn_item_list.grid(row=0, column=1, padx=0, pady=0, ipady=3, ipadx=5)
        self.image_end_of_day = tk.PhotoImage(file='images/accounting.png')
        self.btn_end_of_day = tk.Button(self.frame_top, text='End of Day', font=('arial', 12, 'bold'),
                                        image=self.image_end_of_day, compound='left', height=50, bg=btn_background)
        self.btn_end_of_day.grid(row=0, column=2, padx=0, pady=0, ipady=3, ipadx=5)
        self.image_reports = tk.PhotoImage(file='images/report.png')
        self.btn_reports = tk.Button(self.frame_top, text='Reports', font=('arial', 12, 'bold'),
                                     image=self.image_reports, compound='left', height=50, bg=btn_background)
        self.btn_reports.grid(row=0, column=3, padx=0, pady=0, ipady=3, ipadx=5)
        self.image_preferences = tk.PhotoImage(file='images/control.png')
        self.btn_preferences = tk.Button(self.frame_top, text='Preferences', font=('arial', 12, 'bold'),
                                         image=self.image_preferences, compound='left', height=50, bg=btn_background)
        self.btn_preferences.grid(row=0, column=4, padx=0, pady=0, ipady=3, ipadx=5)
        self.image_about = tk.PhotoImage(file='images/about.png')
        self.btn_about = tk.Button(self.frame_top, text='About', font=('arial', 12, 'bold'), image=self.image_about,
                                   compound='left', height=50, bg=btn_background)
        self.btn_about.grid(row=0, column=5, padx=0, pady=0, ipady=3, ipadx=5)


class ItemList(tk.Frame):
    def __init__(self, container):
        super().__init__(container)

        # Center left frame
        self.left_frame = tk.Frame(root.frame_center, relief='sunken', bg='#e0f0f0', borderwidth=2)
        self.left_frame.grid(row=0, column=0, sticky='news')

        # Center right frame
        self.right_frame = tk.Frame(root.frame_center, relief='sunken', bg='#e0f0f0', borderwidth=2, width=450)
        self.right_frame.grid(row=0, column=1, sticky='news')
        self.right_frame.rowconfigure(0, weight=0)
        self.right_frame.rowconfigure(1, weight=1)
        self.right_frame.columnconfigure(0, weight=1)

        # Search bar
        self.search_bar = tk.LabelFrame(self.right_frame, text='Search Box', bg='#9bc9ff', width=440, height=75)
        self.search_bar.grid(row=0, column=0, sticky='new')
        # Search label
        self.lbl_search = tk.Label(self.search_bar, text='Search :', font=('arial', 12, 'bold'), bg='#9bc9ff',
                                   fg='white')
        self.lbl_search.grid(row=0, column=0, padx=20, pady=10)
        # Search entry
        self.ent_search = tk.Entry(self.search_bar, width=30, bd=10)
        self.ent_search.grid(row=0, column=1, columnspan=3, padx=10, pady=10)
        # Search button
        self.btn_search = tk.Button(self.search_bar, text='Search', font=('arial', 12), bg='#fcc324', fg='white')
        self.btn_search.grid(row=0, column=4, padx=20, pady=10)
        # List bar
        self.list_bar = tk.LabelFrame(self.right_frame, text='List Box', bg='#fcc324', width=440, height=175)
        self.list_bar.grid(row=1, column=0, sticky='new')
        self.lbl_list = tk.Label(self.list_bar, text='Sort By', font=('times', 16, 'bold'), fg='#2488ff', bg='#fcc324')
        self.lbl_list.grid(row=0, column=2)
        self.list_choice = tk.IntVar()
        self.rb1 = tk.Radiobutton(self.list_bar, text='Title', variable=self.list_choice, value='first option',
                                  bg='#fcc324')
        self.rb2 = tk.Radiobutton(self.list_bar, text='Author', variable=self.list_choice, value=2, bg='#fcc324')
        self.rb1.grid(row=1, column=0)
        self.rb2.grid(row=1, column=1)
        self.btn_list = tk.Button(self.list_bar, text='List Books', bg='#2488ff', fg='white', font='arial 12')
        self.btn_list.grid(row=1, column=3, padx=40, pady=10)

        # title and image
        self.image_bar = tk.Frame(self.right_frame, width=440, height=350)
        self.image_bar.grid(sticky='news')
        self.title_right = tk.Label(self.image_bar, text='Cambridge Point of Sale', font='arial 16 bold')
        self.title_right.grid(row=0)
        self.img_library = tk.PhotoImage(file='images/library.png')
        self.lblImg = tk.Label(self.image_bar, image=self.img_library)
        self.lblImg.grid(row=1)


# Root window
root = Application()

root.mainloop()
