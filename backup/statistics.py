import tkinter as tk


root = tk.Tk()

x_bar_label = tk.Label(text='X bar')
x_bar_label.grid(row=0, column=0)
x_bar = tk.Entry()
x_bar.grid(row=0, column=1)

x_bar_label = tk.Label(text='N')
x_bar_label.grid(row=1, column=0)
x_bar = tk.Entry()
x_bar.grid(row=1, column=1)

x_bar_label = tk.Label(text='a')
x_bar_label.grid(row=2, column=0)
x_bar = tk.Entry()
x_bar.grid(row=2, column=1)

x_bar_label = tk.Label(text='Sigma')
x_bar_label.grid(row=3, column=0)
x_bar = tk.Entry()
x_bar.grid(row=3, column=1)

# a1 = 1-a
# a2 = a1/2


CI = tk.Label(text='')

button = tk.Button(text='Calculate')
button.grid(row=4, column=0)
root.mainloop()
