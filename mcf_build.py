import tkinter as tk
import os
from itertools import cycle
from modules import mcf_singleton
from modules import mcf_styles
from modules import (
    mcf_gamechecker,
    mcf_aram,
    mcf_featured,
    mcf_tophead
)

from mcf_data import (
    ALL_CHAMPIONS_IDs,
    APP_ICON_PATH,
    APP_TITLE,
    BACKGROUND_IMAGES_PATH,
    BUTTONS_PATH,
    LOADING_STOP_PATH,
    LOADING_START_PATH,
    CHARARACTER_ICON_PATH,
    currentGameData,
    Switches

)

class MCFWindow(tk.Tk, mcf_singleton.Singleton):
    def init(self):
        super().__init__()
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
        self.loading_images = (
            tk.PhotoImage(file=LOADING_STOP_PATH),
            tuple(tk.PhotoImage(file=LOADING_START_PATH.format(index=i)) for i in range(1, 31))
        )
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
        self.character_icons = {
            name: tk.PhotoImage(file=os.path.join(CHARARACTER_ICON_PATH, f'{name}.png')) for name in ALL_CHAMPIONS_IDs.values()
            if name not in ('Kayn_b')
        }
        self.canvas = MCFCanvas(self)
        self.info_view = MCFInfo(self)
        self.obj_aram = mcf_aram.MCF_Aram(self)
        self.obj_featured = mcf_featured.MCF_Featured(self)
        self.obj_gamechecker = mcf_gamechecker.MCF_Gamechecker(self)
        self.obj_tophead = mcf_tophead.MCF_Tophead(self, self.canvas)
        self.rmc_menu = RMCMenu(self, self.canvas)
        
    def refresh(self):
        """
            Clearing all widgets and data in entrys

        """
        Switches.request = False
        self.obj_gamechecker.refresh()
        ...

    def __init__(self):
        ...

class MCFCanvas(tk.Canvas, mcf_singleton.Singleton):
    def init(self, master: MCFWindow):
        super().__init__()
        # self.parent = master
        self.background_objects = {
            "background": self.create_image(0, 0, image=master.background_image, anchor=tk.NW),
            "skeleton": self.create_image(0, 0, image=master.skeleton_image, anchor=tk.NW),
            "loading": self.create_image(465, 388, image=master.loading_images[0], anchor=tk.NW),
            "aram": self.create_image(4, 156, image=self.master.aram_image, anchor=tk.NW, tag='34'),
            "rift": self.create_image(100, 156, image=self.master.rift_image, anchor=tk.NW)
        }
        self.temp_photoimage = None
        self.config(
            width=500,
            height=420,
            highlightthickness=0
        )
        
        self.place(x=0, y=0, relheight=1, relwidth=1)

    def start_circle(self):
        cycle_loading = cycle(self.master.loading_images[1])

        def _update_circle():
        
            if not Switches.request:
                self.delete(self.background_objects['loading'])
                self.background_objects['loading'] = self.create_image(465, 388, image=self.master.loading_images[0], anchor=tk.NW)
                return

            image = next(cycle_loading)
            self.delete(self.background_objects['loading'])
            self.background_objects['loading'] = self.create_image(465, 388, image=image, anchor=tk.NW)
            self.after(65, _update_circle)
        _update_circle()

    def change_background_image(self, character):
        for img in self.background_objects.values():
            self.delete(img)

        self.temp_photoimage = tk.PhotoImage(file=os.path.join(BACKGROUND_IMAGES_PATH, f'{character}.png'))
        
        self.background_objects = {
            "background": self.create_image(0, 0, image=self.temp_photoimage, anchor=tk.NW),
            "skeleton": self.create_image(0, 0, image=self.master.skeleton_image, anchor=tk.NW),
            "loading": self.create_image(465, 388, image=self.master.loading_images[0], anchor=tk.NW),
            "aram": self.create_image(4, 156, image=self.master.aram_image, anchor=tk.NW, tag='34'),
            "rift": self.create_image(100, 156, image=self.master.rift_image, anchor=tk.NW)
           
        }
    
    def get_icon_photoimage(character):
    
        return tk.PhotoImage(file=os.path.join(CHARARACTER_ICON_PATH, f'{character}.png'))

    def __init__(self, master):
         ...
 
class MCFInfo(tk.Frame, mcf_singleton.Singleton):
    def init(self, master: MCFWindow) -> None:    
        tk.Frame.__init__(self, master)
        self.info_image = tk.Label(master, 
                                   image=master.button_images['i_label'], 
                                   borderwidth=0, 
                                   highlightthickness=2, 
                                   highlightbackground='#cc9c1b',
                                    )
        self.info_label = mcf_styles.Label(height=1, hlb='#cc9c1b', hlt=2)

        self.info_image.pack(in_=self, side='left')
        self.info_label.pack(in_=self, side='right')
    
    def hide_info(self):
        self.place_forget()

    def display_info(self, text, ground='yellow', delay: int = None):

        if Switches.after_info[0] is not None:
            self.master.after_cancel(Switches.after_info[0])
            
        self.info_label['text'] = f' {text} '
        self.info_label['highlightbackground'] = ground
        self.info_image['highlightbackground'] = ground
        self.place(x=125, y=0)

        if delay:
            Switches.after_info[0] = self.master.after(int(delay * 1000), self.hide_info)
    
    def __init__(self, master) -> None:
        ...

class RMCMenu(tk.Frame):
    def __init__(self, supermaster: MCFWindow, master: MCFCanvas):
        tk.Frame.__init__(self, supermaster)
        # self.parent = master
        self.config(
            highlightthickness=1,
            highlightbackground='#1aaeb0'
        )

        supermaster.bind('<Button 3>', lambda e: self.show(master))
        master.bind('<Button 1>', lambda e: self.place_forget())
        self.buttons = {}
    
    def show(self: tk.Frame, master: MCFCanvas):
        x = master.winfo_pointerx() - master.winfo_rootx()
        y = master.winfo_pointery() - master.winfo_rooty()
        self.place(x=x, y=y)
        
    def add_command(self, text, command, button_forget=True, switch_button=False):
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
    
        
        
