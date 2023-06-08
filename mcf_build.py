import tkinter as tk
import os
from modules import mcf_singleton
from modules import mcf_styles
from modules import mcf_aram
from modules import mcf_featured
from modules import mcf_tophead
from modules import mcf_gamechecker
from mcf_data import (
    APP_ICON_PATH,
    APP_TITLE,
    BACKGROUND_IMAGES_PATH,
    BUTTONS_PATH,
    Switches

)

class MCFWindow(tk.Tk, mcf_singleton.Singleton):
    def __init__(self):
        tk.Tk.__init__(self)
        self.wm_attributes('-topmost', True)
        self.title(APP_TITLE)
        self.resizable(False, False)
        self.geometry(f'500x420+100+100')
        self.icon = tk.PhotoImage(file=APP_ICON_PATH)
        self.iconphoto(False, self.icon)
        self.aram_image = tk.PhotoImage(file=os.path.join(BACKGROUND_IMAGES_PATH, 'skeleton_aram.png'))
        self.rift_image = tk.PhotoImage(file=os.path.join(BACKGROUND_IMAGES_PATH, 'skeleton_classic.png'))
        self.skeleton_image = tk.PhotoImage(file=os.path.join(BACKGROUND_IMAGES_PATH, 'skeleton_advance.png'))
        self.background_image = tk.PhotoImage(file=os.path.join(BACKGROUND_IMAGES_PATH, 'Custom.png'))
        self.button_images = {
            'Kindred': tk.PhotoImage(file=BUTTONS_PATH + 'Kindred_btn.png'),
            'Vayne': tk.PhotoImage(file=BUTTONS_PATH + 'Vayne_btn.png'),
            'TF': tk.PhotoImage(file=BUTTONS_PATH + 'TF_btn.png'),
            'Leblanc': tk.PhotoImage(file=BUTTONS_PATH + 'Leblanc_btn.png'),
            'Annie': tk.PhotoImage(file=BUTTONS_PATH + 'Annie_btn.png'),
            'Diana': tk.PhotoImage(file=BUTTONS_PATH + 'Diana_btn.png'),
            'Custom': tk.PhotoImage(file=BUTTONS_PATH + 'Custom_btn.png'),
            'Stats': tk.PhotoImage(file=BUTTONS_PATH + '_stats_btn.png'),
            'Magic': tk.PhotoImage(file=BUTTONS_PATH + '_magic_btn.png'),
            'ARAM': tk.PhotoImage(file=BUTTONS_PATH + '_aram_sbtn.png'),
            'Rift': tk.PhotoImage(file=BUTTONS_PATH + '_classic_sbtn.png'),
            '1X_Game': tk.PhotoImage(file=BUTTONS_PATH + '_xgame_btn.png'),
            'Normal': tk.PhotoImage(file=BUTTONS_PATH + '_normal_sbtn.png'),
            'Delayed': tk.PhotoImage(file=BUTTONS_PATH + '_delayed_sbtn.png'),
            'Ground': tk.PhotoImage(file=BUTTONS_PATH + '_background_btn.png'),
            'i_label': tk.PhotoImage(file=BUTTONS_PATH + '_i_label.png'),
            'x_label': tk.PhotoImage(file=BUTTONS_PATH + '_x_label.png'),
            'Get': tk.PhotoImage(file=BUTTONS_PATH + '_get_btn.png'),
            'Search': tk.PhotoImage(file=BUTTONS_PATH + '_search_btn.png'),
            'Arrow': tk.PhotoImage(file=BUTTONS_PATH + '_arrow_btn.png'),
            'Run': tk.PhotoImage(file=BUTTONS_PATH + '_run_btn.png'),
            'Spec': tk.PhotoImage(file=BUTTONS_PATH + '_spec_btn.png'),
            'calculate': tk.PhotoImage(file=BUTTONS_PATH + '_calculate_btn.png'), 
        }
        # self.background_image = 'Custom.png'

class MCFCanvas(tk.Canvas):
    def __init__(self, master):
        tk.Canvas.__init__(self, master)
        self.config(
            width=500,
            height=420,
            highlightthickness=0
        )
        self.place(x=0, y=0, relheight=1, relwidth=1)
        self.background_image = tk.PhotoImage(file=os.path.join(BACKGROUND_IMAGES_PATH, 'Custom.png'))
        self.skeleton = tk.PhotoImage(file=os.path.join(BACKGROUND_IMAGES_PATH, 'skeleton_advance.png'))
        self.obj_tophead = mcf_tophead.MCF_Tophead(master)
        self.obj_aram = mcf_aram.MCF_Aram(master)
        self.obj_featured = mcf_featured.MCF_Featured(master)
        self.obj_gamechecker = mcf_gamechecker.MCF_Gamechecker(master)
        self.info_view = MCFInfo(master)
        self.rmc_menu = RMCMenu(master, self)
        
        self.create_background(master)
        self.place_app_buttons()

        self.rmc_menu.add_command('Refresh', 
                                  command=lambda: self.info_view.display_info(self, text='Refresh command', ground='green', delay=2.5))
        self.bind('<Button 3>', lambda e: self.rmc_menu.show(master))
        
    def place_app_buttons(self):
        
        self.obj_tophead.stats.place(x=0, y=0)
        self.obj_tophead.magic.place(x=62, y=0)
        self.obj_tophead.ground.place(x=439, y=0)

        self.obj_aram.blue_entry.place(x=38, y=52)
        self.obj_aram.red_entry.place(x=38, y=78)
        self.obj_aram.calculate.place(x=415, y=121)

        self.obj_featured.parsed_aram_entry.place(x=16, y=253)
        self.obj_featured.parsed_rift_entry.place(x=111, y=253)
        self.obj_featured.character_rift.place(x=111, y=183)
        self.obj_featured.aram_get_button.place(x=24, y=208)
        self.obj_featured.rift_get_button.place(x=119, y=210)

        self.obj_gamechecker.entry.place(x=11, y=343)
        self.obj_gamechecker.search_button.place(x=11, y=370)
        self.obj_gamechecker.arrow_button.place(x=120, y=370)

    def create_background(self, master):
        self.create_image(0, 0, image=master.background_image, anchor=tk.NW)
        self.create_image(0, 0, image=master.skeleton_image, anchor=tk.NW),
        # self.create_image(465, 388, image=self.loading_objects[0], anchor=tk.NW)
 
class MCFInfo:
    def __init__(self, master) -> None:
        self.info_image = tk.Label(master, 
                                   image=master.button_images['i_label'], 
                                   borderwidth=0, 
                                   highlightthickness=2, 
                                   highlightbackground='#cc9c1b')
        self.info_label = mcf_styles.Label(height=1, hlb='#cc9c1b', hlt=2)
    
    def hide_info(self):
        self.info_label.place_forget()
        self.info_image.place_forget()

    def display_info(self, master, text, ground, delay: int = None):

        if Switches.after_info[0] is not None:
            master.after_cancel([0])
            
        self.info_label['text'] = f' {text} '
        self.info_label['highlightbackground'] = ground
        self.info_image['highlightbackground'] = ground
        self.info_label.place(x=143, y=1)
        self.info_image.place(x=125, y=1)

        if delay:
            Switches.after_info[0] = master.after(int(delay * 1000), self.hide_info)

class RMCMenu(tk.Frame):
    def __init__(self, master, slave):
        tk.Frame.__init__(self, master)
        self.config(
            highlightthickness=1,
            highlightbackground='#1aaeb0'
        )
        slave.bind('<Button 1>',lambda e: self.place_forget())

        self.buttons = {}
        
    def show(self, master):
        
        x = master.winfo_pointerx() - master.winfo_rootx()
        y = master.winfo_pointery() - master.winfo_rooty()
        self.place(x=x, y=y, bordermode='inside')
        
    def add_command(self, text, command, button_forget=False, switch_button=False):
        kwargs = {
            'text': text,
            'command': command,
            'fg': 'black',
            'font': ('Tahoma', 8, 'bold'),
            'bd': 0,
            'highlightthickness': 1,
            'highlightcolor': 'blue',
            'width': 15
        }

        if button_forget:
            kwargs['command'] = lambda: [command(), self.place_forget()]
        
        self.buttons[text] = tk.Button(self, **kwargs)
        self.buttons[text].bind('<Enter>', lambda e: self.buttons[text].config(bg='#1aaeb0'))
        self.buttons[text].bind('<Leave>', lambda e: self.buttons[text].config(bg='white'))
        self.buttons[text].pack()
    
        
        
