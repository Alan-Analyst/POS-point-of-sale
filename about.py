import customtkinter as ct
import webbrowser


class About(ct.CTkFrame):
    def __init__(self, container, controller):
        super().__init__(container)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=0)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.textbox = ct.CTkTextbox(master=self, width=400, corner_radius=0, fg_color='transparent', height=100,
                                     font=ct.CTkFont(size=18))
        self.textbox.grid(row=0, column=0, sticky="news", pady=10, padx=10, columnspan=2)
        self.textbox.insert("0.0", """I am Alan, a Python developer with two years of experience in data analytics and 
back-end development. In my free time, I enjoy building cool apps like this one, which is completely free to use!
If you'd like to learn more about me and check out more of my cool apps, please visit my website at 
https://alananalyst.com/. Thank you for using my app!""")

        self.btn_visit_website = ct.CTkButton(self, text='Vist Website', command=open_link, height=40)
        self.btn_visit_website.grid(row=1, column=0, pady=10, sticky='NE', padx=5)

        self.btn_visit_website = ct.CTkButton(self, text='Report a Bug', command=report_a_bug, height=40)
        self.btn_visit_website.grid(row=1, column=1, pady=10, sticky='NW', padx=5)

        self.textbox._scrollbars_activated = False
        self.textbox.configure(state='disabled')


def report_a_bug():
    # Replace 'recipient' with the email address of the recipient
    # and 'subject' with the email subject
    url = 'mailto:alananalyst00@gmail.com?subject=Bug in POS'

    # Open the email client
    webbrowser.open(url)


def open_link():
    webbrowser.open("https://www.alananalyst.com")
