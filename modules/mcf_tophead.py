import tkinter as tk
from modules import mcf_styles

class MCF_Tophead:
    def __init__(self, master) -> None:
        self.stats = mcf_styles.Button(display=master.button_images['Stats'])
        self.magic = mcf_styles.Image(display=master.button_images['Magic'])
        self.magic_aram = mcf_styles.Button(display=master.button_images['ARAM'])
        self.magic_rift = mcf_styles.Button(display=master.button_images['Rift'])
        self.ground = mcf_styles.Image(display=master.button_images['Ground'])
    
    def display_stats():
        ...
    
    def compare_icons():
        ...
    
    def reveal_possible_backgrounds():
        ...