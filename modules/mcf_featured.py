import tkinter as tk
import time
from modules import mcf_styles
from mcf_build import MCFWindow, MCFException
from mcf_threads import MCFThread
from mcf_riot_api import PoroAPI
from .mcf_decortators import disable_button_while_running
from mcf_data import (
    ALL_CHAMPIONS_IDs,
)

class MCF_Featured():
    def __init__(self, master: MCFWindow) -> None:
        self.parent = master
        self.frames = tuple(tk.LabelFrame(bd=0,
                                          highlightthickness=1,
                                          highlightbackground='#339999') 
                            for _ in range(0, 5))
        self.entry_aram_for_storage = mcf_styles.Entry(width=12)
        self.entry_aram_for_storage.bind("<Return>", lambda e: self.show_parsed_games(state='aram_api'))
        self.entry_poro_for_parse = mcf_styles.Entry(width=12)
        self.entry_poro_for_parse.bind("<Return>", lambda e: MCFThread(func=self.parse_rift_games).start())

        self.button_aram_get = mcf_styles.Button(display=master.button_images['Get'],
                                                 command=lambda: MCFThread(func=self.parse_aram_games).start())
        
        self.button_rift_get = mcf_styles.Button(display=master.button_images['Get'],
                                                 command=lambda: MCFThread(func=self.parse_rift_games).start())
        
        self.button_featured_games = tuple(mcf_styles.Button(i) for i in self.frames)

        self.entry_aram_for_storage.place(x=5, y=253)
        self.entry_poro_for_parse.place(x=99, y=253)
        self.button_aram_get.place(x=24, y=198)
        self.button_rift_get.place(x=117, y=200)

    def _refresh(self):
        for frame in self.frames:
            frame.place_forget()

        self.entry_aram_for_storage.delete(0, 'end')
        self.entry_poro_for_parse.delete(0, 'end')

    def _frames_config(self, button: mcf_styles.Button, data: str):

        def create_command_for_button(nickname):
            self.parent.obj_gamechecker.entry.delete(0, 'end')
            self.parent.obj_gamechecker.entry.insert(0, nickname)

            for frame in self.frames:
                frame.place_forget()

        characters, nickname = data.split('-|-')

        button.configure(
            command= lambda: create_command_for_button(nickname.split('_|_')[0]),
            text=characters
        )

    @disable_button_while_running(object_='obj_featured',
                                  buttons=('button_aram_get', 'button_rift_get'))
    def parse_aram_games(self):
        from .scripts import async_featured_games
        
        self.parent.info_view.notification('Wait...')

        missing_regions = async_featured_games.parse_games()
        match missing_regions:
            case 0:
                self.parent.info_view.success('Done')
            case 20:
                self.parent.info_view.exception('No connection')
            case count:
                self.parent.info_view.success(f'Done | Missing regs: {count}')
    
    @disable_button_while_running(object_='obj_featured',
                                  buttons=('button_aram_get', 'button_rift_get'))
    def parse_rift_games(self):

        from .scripts import storage_data
        
        try:
            player_red, player_blue = self.entry_poro_for_parse.get().split('-')
        except ValueError:
            self.parent.info_view.exception('Use "-" between characters')
            return

        self.parent.info_view.notification('Wait...')
        
        try:
            PoroAPI.get_poro_games(red_champion=player_red)
            self.parent.info_view.success('Done')

        except MCFException as ex:
            self.parent.info_view.exception(str(ex))
            return

        time.sleep(0.25)

        from .scripts import storage_data

        # print(player_blue, player_red)
        try:
            games_by_character = storage_data.get_games_by_character(character=player_blue, state='aram_poro_2') # Characters-|-nickname:region
        except MCFException as ex:
            self.parent.info_view.exception(str(ex))
            games_by_character = None

        if games_by_character is not None:
            if self.frames[0].winfo_viewable() == 1:

                for frame in self.frames: 
                    frame.place_forget()

            for i, y in zip(range(len(games_by_character)), [152, 177, 202, 227, 252]):
                self._frames_config(button=self.button_featured_games[i],
                                    data=games_by_character[i])
            
                match self.button_aram_get.winfo_viewable():
                    case 1:
                        self.frames[i].place(x=190, y=y)
                    case 0:
                        self.frames[i].place(x=70, y=y)
                    case _:
                        pass
            
    
    def show_parsed_games(self, state: str = ''):
        from .scripts import storage_data

        if state == 'aram_api':
            character = self.entry_aram_for_storage.get()
        else:
            character = self.entry_rift_for_storage.get()

        try:
            games_by_character = storage_data.get_games_by_character(character=character, state=state) # Characters-|-nickname:region
        except MCFException as ex:
            self.parent.info_view.exception(str(ex))
            games_by_character = None

        if games_by_character is not None:
            if self.frames[0].winfo_viewable() == 1:

                for frame in self.frames: 
                    frame.place_forget()

            for i, y in zip(range(len(games_by_character)), [152, 177, 202, 227, 252]):
                self._frames_config(button=self.button_featured_games[i],
                                    data=games_by_character[i])
            
                match self.button_aram_get.winfo_viewable():
                    case 1:
                        self.frames[i].place(x=190, y=y)
                    case 0:
                        self.frames[i].place(x=70, y=y)
                    case _:
                        pass
        