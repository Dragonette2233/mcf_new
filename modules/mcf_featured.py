import tkinter as tk
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
        self.entry_aram_for_storage = mcf_styles.Entry(width=9)
        self.entry_aram_for_storage.bind("<Return>", lambda e: self.show_parsed_games(aram=True))

        self.entry_rift_for_storage = mcf_styles.Entry(width=9)
        self.entry_rift_for_storage.bind("<Return>", lambda e: self.show_parsed_games(aram=False))

        self.entry_rift_for_parse = mcf_styles.Entry(width=9)
        self.entry_rift_for_parse.bind("<Return>", lambda e: MCFThread(func=self.parse_rift_games).start())

        self.button_aram_get = mcf_styles.Button(display=master.button_images['Get'],
                                                 command=lambda: MCFThread(func=self.parse_aram_games).start())
        
        self.button_rift_get = mcf_styles.Button(display=master.button_images['Get'],
                                                 command=lambda: MCFThread(func=self.parse_rift_games).start())
        
        self.button_featured_games = tuple(mcf_styles.Button(i) for i in self.frames)

        self.entry_aram_for_storage.place(x=16, y=253)
        self.entry_rift_for_storage.place(x=111, y=253)
        self.entry_rift_for_parse.place(x=111, y=183)
        self.button_aram_get.place(x=24, y=208)
        self.button_rift_get.place(x=119, y=210)

    def _refresh(self):
        for frame in self.frames:
            frame.place_forget()

        self.entry_aram_for_storage.delete(0, 'end')
        self.entry_rift_for_storage.delete(0, 'end')
        self.entry_rift_for_parse.delete(0, 'end')

    def _frames_config(self, button: mcf_styles.Button, data: str):

        def create_command_for_button(nickname):
            self.parent.obj_gamechecker.entry.delete(0, 'end')
            self.parent.obj_gamechecker.entry.insert(0, nickname)

            for frame in self.frames:
                frame.place_forget()

        characters, nickname = data.split('-|-')

        button.configure(
            command= lambda: create_command_for_button(nickname),
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

        self.parent.info_view.notification('Wait...')
        try:
            PoroAPI.get_poro_games(red_champion=self.entry_rift_for_parse.get(), gamemode='aram')
            self.parent.info_view.success('Done')

        except MCFException as ex:
            self.parent.info_view.exception(str(ex))
            
    
    def show_parsed_games(self, aram: bool):
        from .scripts import storage_data

        if aram:
            character = self.entry_aram_for_storage.get()
        else:
            character = self.entry_rift_for_storage.get()

        try:
            games_by_character = storage_data.get_games_by_character(character=character, aram=aram) # Characters-|-nickname:region
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
        