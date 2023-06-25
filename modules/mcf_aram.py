from modules import mcf_styles
from .scripts import stats_by_roles
from mcf_build import MCFWindow, MCFException
from mcf_data import ALL_CHAMPIONS_IDs, MCFStorage

def unready_command():
    print('Buttons is working fine!')

class MCF_Aram():
    def __init__(self, master: MCFWindow) -> None:
        self.parent = master
        self.blue_entry = mcf_styles.Entry(width=24)
        self.red_entry = mcf_styles.Entry(width=24)
        self.calculate = mcf_styles.Button(display=master.button_images['calculate'],
                                           command=self.get_aram_statistic)
        self.blue_win = mcf_styles.StatsRateLabel()
        self.red_win = mcf_styles.StatsRateLabel()
        self.total_bigger = mcf_styles.StatsRateLabel()
        self.total_lower = mcf_styles.StatsRateLabel()
        self.blue_diplay = mcf_styles.DisplayBlueButton()
        self.red_display = mcf_styles.DisplayRedLabel()
        self.matches_all = mcf_styles.Label(fsize=10, width=4, hlt=1, hlb='#9966cc')
        self.matches_by_total = mcf_styles.Label(fsize=10, width=4, hlt=1, hlb='#9966cc')

        self.blue_entry.place(in_=master, x=38, y=52)
        self.red_entry.place(x=38, y=78)
        self.calculate.place(x=415, y=121)
    
    def get_aram_statistic(self):
        try:
            
            refactored_blue = self.parent.find_characters_name(
                characters_list=self.blue_entry.get().strip().split(' '))
            refactored_red = self.parent.find_characters_name(
                characters_list=self.red_entry.get().split(' ')
            )

            self.parent.place_character_icons((*refactored_blue, *refactored_red), activegame=False, place=1)
        
            rate_and_colors = stats_by_roles.get_aram_statistic(
                blue_entry=refactored_blue,
                red_entry=refactored_red,
            )
            self.blue_win.configure(
                text=rate_and_colors['w1'][0],
                fg=rate_and_colors['w1'][1]
            )
            self.red_win.configure(
                text=rate_and_colors['w2'][0],
                fg=rate_and_colors['w2'][1]
            )
            self.total_bigger.configure(
                text=rate_and_colors['tb'][0],
                fg=rate_and_colors['tb'][1]
            )
            self.total_lower.configure(
                text=rate_and_colors['tl'][0],
                fg=rate_and_colors['tl'][1]
            )
            self.matches_all.configure(
                text=rate_and_colors['all_m'][0],
                fg=rate_and_colors['all_m'][1]
            )
            self.matches_by_total.configure(
                text=rate_and_colors['all_ttl'][0],
                fg=rate_and_colors['all_ttl'][1]
            )
            
            self.blue_win.place_configure(x=215, y=52)
            self.red_win.place_configure(x=215, y=78)
            self.total_bigger.place_configure(x=48, y=108)
            self.total_lower.place_configure(x=193, y=108)
            self.matches_all.place_configure(x=77, y=31)
            self.matches_by_total.place_configure(x=153, y=31)
            
        except MCFException as ex:
            self.parent.info_view.exception(str(ex))

        
    def refill_characters_entrys(self, blue_chars, red_chars):
        self.blue_entry.delete(0, 'end')
        self.red_entry.delete(0, 'end')
        self.blue_entry.insert(0, blue_chars)
        self.red_entry.insert(0, red_chars)

    def _refresh(self):
        self.blue_entry.delete(0, 'end')
        self.red_entry.delete(0, 'end')
        self.blue_win.place_forget()
        self.red_win.place_forget()
        self.total_bigger.place_forget()
        self.total_lower.place_forget()
        self.matches_all.place_forget()
        self.matches_by_total.place_forget()
    