import tkinter as tk
from modules import mcf_styles

class MCF_Featured():
    def __init__(self, master) -> None:
        self.parent = master
        self.frames = tuple(tk.LabelFrame(bd=0,
                                          highlightthickness=1,
                                          highlightbackground='#339999') 
                            for _ in range(0, 5))
        self.parsed_aram_entry = mcf_styles.Entry(width=9)
        self.parsed_aram_entry.bind("<Return>", lambda e: self.show_parsed_games(aram=True))

        self.parsed_rift_entry = mcf_styles.Entry(width=9)
        self.parsed_rift_entry.bind("<Return>", lambda e: self.show_parsed_games())

        self.character_rift = mcf_styles.Entry(width=9)
        self.character_rift.bind("<Return>", lambda e: self.parse_rift_games(bindaction=True))

        self.aram_get_button = mcf_styles.Button(display=master.button_images['Get'],
                                                 command=self.parse_aram_games)
        
        self.rift_get_button = mcf_styles.Button(display=master.button_images['Get'],
                                                 command=self.parse_rift_games)
        
        self.games_avaliable_buttons = tuple(mcf_styles.Button(i) for i in self.frames)

        self.parsed_aram_entry.place(x=16, y=253)
        self.parsed_rift_entry.place(x=111, y=253)
        self.character_rift.place(x=111, y=183)
        self.aram_get_button.place(x=24, y=208)
        self.rift_get_button.place(x=119, y=210)

    def parse_aram_games(self):
        print('In parsing aram game func')
    
    def parse_rift_games(self, bindaction=False):
        if bindaction:
            print('In parsing rift game func with bind on return')
        else:
            print('In parsing rift game func')
    
    def show_parsed_games(self, aram=False):
        if aram:
            print('In showing parsed aram games func')
        else:
            print('In showing parsed rift games func')