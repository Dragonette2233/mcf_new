import tkinter as tk

class Button(tk.Button):
    def __init__(self, master=None, display=None, command=None, args=None, width=None):
        tk.Button.__init__(self, master)
        
        self.config(
            font=('Calibri', 9),
            width=width,
            image=display,
            borderwidth=0,
            highlightthickness=0,
            bg='#370d3d',
            fg='white',
            command=command,
        )
        if args:
            self.config(command=lambda: command(*args))
        
        if isinstance(master, tk.LabelFrame):
            self.pack()
        
        self.bind('<Enter>', lambda e: self.config(bg='#652f87'))
        self.bind('<Leave>', lambda e: self.config(bg='#370d3d'))

class Label(tk.Label):
    def __init__(self, fsize=8, height=None, hlb=None, width=None, text=None, hlt=2):
        tk.Label.__init__(self)
        self.config(
            bd=0,
            bg='#370d3d',
            font=('Tahoma', fsize, 'bold'),
            fg='white',
            highlightthickness=hlt,
            highlightbackground=hlb,
            width=width,
            text=text
        )
        if height is not None:
            self.config(height=height)

class Image(tk.Label):
    def __init__(self, display, lunge=None, args=None):
        tk.Label.__init__(self)
        self.config(
            image=display,
            borderwidth=0,
            highlightthickness=0,
            bg='#370d3d'
        )

        self.bind('<Enter>', lambda e: self.config(bg='#652f87'))
        self.bind('<Leave>', lambda e: self.config(bg='#370d3d'))

class StatsRateLabel(tk.Label):
    def __init__(self, width=6):
        tk.Label.__init__(self)
        self.config(
            font=('Tahoma', 8, 'bold'),
            bg='#370d3d',
            highlightthickness=1,
            highlightbackground='#9966cc',
            width=width)

class Entry(tk.Entry):
    def __init__(self, width):
        tk.Entry.__init__(self)
        self.config(
            width=width,
            highlightthickness=1,
            highlightcolor='#3AAACF',
            highlightbackground='#4D54D8',
            font=('Calibri', 10, 'bold')
        )