import tkinter as tk
from modules import mcf_styles

def unready_command():
    print('Buttons is working fine!')

class MCF_Aram():
    def __init__(self, master) -> None:
        self.blue_entry = mcf_styles.Entry(width=24)
        self.red_entry = mcf_styles.Entry(width=24)
        self.calculate = mcf_styles.Button(display=master.button_images['calculate'])
        self.blue_win = mcf_styles.StatsRateLabel()
        self.red_win = mcf_styles.StatsRateLabel()
        self.total_bigger = mcf_styles.StatsRateLabel()
        self.total_lower = mcf_styles.StatsRateLabel()
        self.blue_diplay = mcf_styles.DisplayBlueButton()
        self.red_display = mcf_styles.DisplayRedLabel()
        self.matches_all = mcf_styles.Label(fsize=10, width=4, hlt=1, hlb='#9966cc')
        self.matches_by_total = mcf_styles.Label(fsize=10, width=4, hlt=1, hlb='#9966cc')