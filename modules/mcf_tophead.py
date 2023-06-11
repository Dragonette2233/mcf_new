import tkinter as tk
from modules import mcf_styles
from tkinter import Event, EventType

class MCF_Tophead:
    def __init__(self, master, canvas) -> None:
        # self.parent = master
        self.stats = mcf_styles.Button(display=master.button_images['Stats'])
        self.magic = mcf_styles.Image(display=master.button_images['Magic'])
        self.magic_dropdown = (
                        mcf_styles.Button(display=master.button_images['ARAM']),
                        mcf_styles.Button(display=master.button_images['Rift'])
        )
        self.ground = mcf_styles.Image(display=master.button_images['Ground'])
        self.ground_dropdown = (
                        mcf_styles.Button(display=master.button_images['Kindred'],
                                          command=lambda: canvas.change_background_image('Kindred')),
                        mcf_styles.Button(display=master.button_images['Vayne'],
                                          command=lambda: canvas.change_background_image('Vayne')),
                        mcf_styles.Button(display=master.button_images['TF'],
                                          command=lambda: canvas.change_background_image('TF')),
                        mcf_styles.Button(display=master.button_images['Leblanc'],
                                          command=lambda: canvas.change_background_image('Leblanc')),
                        mcf_styles.Button(display=master.button_images['Annie'],
                                          command=lambda: canvas.change_background_image('Annie')),
                        mcf_styles.Button(display=master.button_images['Diana'],
                                          command=lambda: canvas.change_background_image('Diana')),
                        mcf_styles.Button(display=master.button_images['Custom'],
                                          command=lambda: canvas.change_background_image('Custom'))
                    )
        self.magic.bind('<Enter>', lambda e: [self.ground.config(bg='#652f87'), self.magic_dropdown_show(e)] )
        self.ground.bind('<Enter>', lambda e: [self.ground.config(bg='#652f87'), self.ground_dropdown_show(e)])
        
        canvas.bind('<Enter>', self.all_dropdown_hide)

        self.stats.place(x=0, y=0)
        self.magic.place(x=62, y=0)
        self.ground.place(x=439, y=0)

    def magic_dropdown_show(self, e: Event):
        for button, y in zip(self.magic_dropdown, range(20, (len(self.ground_dropdown) + 1) * 20, 20)):
            button.place(x=62, y=y)

    def ground_dropdown_show(self, e: Event):
        for button, y in zip(self.ground_dropdown, range(20, (len(self.ground_dropdown) + 1) * 20, 20)):
            button.place(x=439, y=y)

    def all_dropdown_hide(self, e: Event):
        for button in *self.ground_dropdown, *self.magic_dropdown:
            button.place_forget()
        
        
    def display_stats():
        ...
    
    def compare_icons():
        ...
    
    def reveal_possible_backgrounds():
        ...