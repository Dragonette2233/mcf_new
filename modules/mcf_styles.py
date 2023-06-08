import tkinter as tk

class Button(tk.Button):
    def __init__(self, display=None, command=None, args=None, width=None):
        tk.Button.__init__(self)
        self.config(
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

    def bound_dropdown_buttons(self, start_x, buttons: tuple[tk.Button]):

        self.bind('<Enter>', lambda e: [self.config(bg='#652f87'), 
                                        [button.place(x=start_x, y=y) for button, y in zip(buttons, [i * 20 for i in range(1, 10)])]])
        
    def place_rightpanel_buttons(self, x, y, panel: tk.Frame):

        self.bind('<Enter>', lambda e: [panel.place(x=x, y=y), self.place_forget()])

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

class DisplayRedLabel(tk.Label):
    def __init__(self):
        tk.Label.__init__(self)
        self.config(
            bd=0,
            highlightbackground='red',
            highlightthickness=2,
        )
    def define_image(self, image, character):
        self.config(image=image, text=character)

class DisplayBlueButton(DisplayRedLabel):
    def __init__(self, command=None):
        DisplayRedLabel.__init__(self)
        self.bind('<Enter>', lambda e: self.config(highlightbackground='#25D500'))
        self.bind('<Leave>', lambda e: self.config(highlightbackground='blue'))
        self.bind('<Button 1>', lambda e: self.config(highlightbackground='white'))
        
    def define_command(self, args, func=None):
        self.bind('<ButtonRelease-1>', lambda e: [DaemonThread(func, args=args).start(), self.config(highlightbackground='#25D500')])