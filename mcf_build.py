import tkinter as tk
import os
import time
from playsound import playsound
from mcf_threads import MCFThread
from itertools import cycle
from modules import mcf_styles
from mcf_riot_api import TGApi
from mcf_data import (
    ALL_CHAMPIONS_IDs,
    APP_ICON_PATH,
    APP_TITLE,
    BACKGROUND_IMAGES_PATH,
    BUTTONS_PATH,
    LOADING_STOP_PATH,
    LOADING_START_PATH,
    CHARARACTER_ICON_PATH,
    TEEMO_SONG_PATH,
    currentGameData,
    Switches,
    MCFStorage,
    MCFException,
    MCFNoConnectionError,
    MCFTimeoutError

)

class Singleton(object):
    def __new__(cls, *args, **kwargs):
        it = cls.__dict__.get("__it__")
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        it.init(*args, **kwargs)
        return it
    
    def init(self, *args, **kwargs):
        ...

class MCFWindow(tk.Tk, Singleton):
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
        self.test_label = tk.Label(self, text=222)
        # print(self.character_icons)
        self.canvas = MCFCanvas(self)
        self.info_view = MCFInfo(self)
        from modules import (
            mcf_tophead, mcf_aram,
            mcf_featured, mcf_gamechecker
        )
        self.obj_featured = mcf_featured.MCF_Featured(self)
        self.obj_aram = mcf_aram.MCF_Aram(self)
        self.obj_tophead = mcf_tophead.MCF_Tophead(self, self.canvas)
        self.obj_gamechecker = mcf_gamechecker.MCF_Gamechecker(self)
        # self.rmc_menu = RMCMenu(self)
        self.context_menu = tk.Menu(tearoff=0)
        self.character_icons = {
            name: tk.PhotoImage(file=os.path.join(CHARARACTER_ICON_PATH, f'{name}.png')) for name in ALL_CHAMPIONS_IDs.values()
            if name != ('Kayn_b')
        }
        print(self.character_icons['Hwei'])
        self.characters_labels = [tk.Label(self, borderwidth=0) for _ in range(0, 10)]
    
    def rmc_callback(self, event):
        self.context_menu.post(event.x_root, event.y_root)

    def aram_porotimer(self):
        from modules.scripts import aram_porotimer_script

        if not Switches.timer:

            Switches.timer = True
            self.info_view._display_info('Waiting for ARAM...', 'blue')

            while Switches.timer:
                game = aram_porotimer_script.start_timer()
                if game is not None:
                    TGApi.display_gamestart(timer=game)
                    self.info_view.notification(game)
                    playsound(TEEMO_SONG_PATH)
                    Switches.timer = False
                    
                    
                time.sleep(4)
        else:
            Switches.timer = False
            self.info_view.notification('Wait...')
            self.after(5200, lambda: self.info_view.exception('ARAM timer stopped'))
       
    def change_calibration_index(self):
    
        match Switches.calibration_index:
            case 0:
                Switches.calibration_index = 1
                self.info_view.success("Calibration 1")
                # text, ground = 'PIL Calibration [1]', '#7718C3'
            case 1:
                Switches.calibration_index = 2
                self.info_view.success("Calibration 2")
                # text, ground = 'PIL Calibration [2]', '#7718C3'
            case 2:
                Switches.calibration_index = 0
                self.info_view.exception("Calibration OFF")
                # text, ground = 'PIL Calibration', 'black'
            case _:
                Switches.calibration_index = 0
                # text, ground = 'PIL Calibration', 'black'
                self.info_view.exception('Unknown error')
        
        # self.rmc_menu.buttons['PIL Calibration'].configure(fg=ground, text=text)
        
    def close_league_of_legends(self):

        list_task = os.popen('tasklist /FI "IMAGENAME eq League of Legends*"').readlines()
        if len(list_task) == 1:
            self.info_view.exception('Game not launched')
            return
        
        list_task[3] = list_task[3].replace(' ', '')
        process_pid = list_task[3].split('exe')[1].split('Console')[0]
        os.popen(f'taskkill /PID {process_pid} /F')
        self.info_view.success('League of Legends closed')

    def find_characters_name(self, characters_list: list[str]):
        """
            Returns a list of characters that match the pattern
            Example: wuk -> Wukong | kha -> Khazix 
        
        """
        
        for i, name in enumerate(characters_list):
            for p in ALL_CHAMPIONS_IDs.values():
                if p.casefold().startswith(name.casefold()) and len(name) != 0:
                    characters_list[i] = p
                    break
            else:
                if len(name) == 0:
                    raise MCFException(f'Error: empty value')
                raise MCFException(f'Error: |{name}| not a character')
            
        return characters_list

    def place_character_icons(self, champions_list: list, activegame=True, place=3):


        if place == 3:
            blue_x = (168, 210, 252, 294, 336)
            blue_y = 300
            red_x = (185, 227, 269, 311, 353)
            red_y = 367
        elif place == 1:
            blue_x = (270, 315, 360, 405, 450)
            blue_y = 31
            red_x = blue_x
            red_y = 77

        """Declaring character icon for label"""
        print(champions_list)
        for i, character in enumerate(champions_list):
            self.characters_labels[i]['image'] = self.character_icons[character]

        """Placing blue team icons"""
        for i, x in zip(range(len(champions_list)), blue_x):
            self.characters_labels[i].place(x=x, y=blue_y)
        
        """Placing red team icons"""
        if len(champions_list) > 5:
            for i, x in zip(range(5, len(champions_list)), red_x):
                self.characters_labels[i].place(x=x, y=red_y)

        # Inserting names in stats entries
        if activegame:
            self.obj_aram.refill_characters_entrys(
                blue_chars = ' '.join(champions_list[0:5]),
                red_chars = ' '.join(champions_list[5:10])
            )
            MCFStorage.write_data(route=('Stats', ),
                                  value={
                                      'T1': champions_list[0:5],
                                      'T2': champions_list[5:10]
                                  })

    def refresh(self):
        """
            Clearing all widgets and data in entrys

        """
        Switches.request = False
        self.obj_aram._refresh()
        self.obj_gamechecker._refresh()
        self.obj_featured._refresh()
        for label in self.characters_labels:
            label.place_forget()
        ...

    def __init__(self):
        ...

class MCFCanvas(tk.Canvas, Singleton):
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
 
class MCFInfo(tk.Frame, Singleton):
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

    def success(self, text):
        self._display_info(text, ground='#32CD32', delay=2)
    
    def notification(self, text):
        self._display_info(text, ground='#87CEEB')
    
    def exception(self, text):
        self._display_info(text, ground='#DC143C', delay=2)
    
    def _display_info(self, text, ground, delay: int = None):

        if Switches.after_info is not None:
            self.master.after_cancel(Switches.after_info)
            
        self.info_label['text'] = f' {text} '
        self.info_label['highlightbackground'] = ground
        self.info_image['highlightbackground'] = ground
        self.place(x=125, y=0)

        if delay:
            Switches.after_info = self.master.after(int(delay * 1000), self.hide_info)
    
    def __init__(self, master) -> None:
        ...

class RMCMenu(tk.Menu):

    def __init__(self, master: MCFWindow):
        tk.Menu.__init__(self, master)
        file_menu = tk.Menu(self, tearoff=0)
        # master.config(menu=self)

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
        
    def add_command(self, text, command, button_forget=True):
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
    
        
        
