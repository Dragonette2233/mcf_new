import tkinter as tk
from modules import mcf_styles
from mcf_threads import MCFThread

class MCF_Featured():
    def __init__(self, master) -> None:
        self.parent = master
        self.frames = tuple(tk.LabelFrame(bd=0,
                                          highlightthickness=1,
                                          highlightbackground='#339999') 
                            for _ in range(0, 5))
        self.parsed_aram_entry = mcf_styles.Entry(width=9)
        self.parsed_aram_entry.bind("<Return>", lambda e: self.show_parsed_games())

        self.parsed_rift_entry = mcf_styles.Entry(width=9)
        self.parsed_rift_entry.bind("<Return>", lambda e: self.show_parsed_games())

        self.character_rift = mcf_styles.Entry(width=9)
        self.character_rift.bind("<Return>", lambda e: self.parse_rift_games(bindaction=True))

        self.aram_get_button = mcf_styles.Button(display=master.button_images['Get'],
                                                 command=lambda: MCFThread(func=self.parse_aram_games).start())
        
        self.rift_get_button = mcf_styles.Button(display=master.button_images['Get'],
                                                 command=self.parse_rift_games)
        
        self.games_avaliable_buttons = tuple(mcf_styles.Button(i) for i in self.frames)

        self.parsed_aram_entry.place(x=16, y=253)
        self.parsed_rift_entry.place(x=111, y=253)
        self.character_rift.place(x=111, y=183)
        self.aram_get_button.place(x=24, y=208)
        self.rift_get_button.place(x=119, y=210)

    def _button_of_frame_command_config(self, nickname):
        # global cnv_images, sw_switches
        # name_region = name_region.split(':')
        # self.parent.obj_(f"{':'.join(name_region[0:2])}", canvas.obj_match_c['entry'])
        self.parent.obj_gamechecker.entry.delete(0, 'end')
        self.parent.obj_gamechecker.entry.insert(0, nickname)

        for frame in self.frames:
            frame.place_forget()

    def _frames_config(self, button: mcf_styles.Button, data: str):

        characters, nickname = data.split('-|-')

        button.configure(
            command= lambda: self._button_of_frame_command_config(nickname),
            text=characters
        )

    def parse_aram_games(self):
        from .scripts import async_featured_games
        
        self.parent.info_view.display_info(text='Wait...')

        missing_regions = async_featured_games.parse_games()
        match missing_regions:
            case 0:
                self.parent.info_view.display_info(text='Done', ground='#25D500', delay=0.75)
            case 16:
                self.parent.info_view.display_info(text='No connection', ground='red', delay=2.5)
            case 20:
                self.parent.info_view.display_info(text='Disable or update proxy', ground='red', delay=2.5)
            case count:
                self.parent.info_view.display_info(text=f'Done | Missing {count} regions', ground='yellow', delay=2.5)
    
    def parse_rift_games(self, bindaction=False):
        if bindaction:
            print('In parsing rift game func with bind on return')
        else:
            print('In parsing rift game func')
    
    def show_parsed_games(self):
        from .scripts import featured_gamelist

        character = self.parsed_aram_entry.get()
        games_by_character = featured_gamelist.get_games_by_character(character=character) # Characters-|-nickname:region

        if self.frames[0].winfo_viewable() == 1:

            for frame in self.frames: 
                frame.place_forget()

        for i, y in zip(range(len(games_by_character)), [152, 177, 202, 227, 252]):
            kwargs = {
                'button': self.games_avaliable_buttons[i],
                'data': games_by_character[i]
            }
            self._frames_config(**kwargs)
            print(len(self.parent.canvas.find_overlapping(4,200,170,160)))

            match len(self.parent.canvas.find_overlapping(4,200,170,160)):
                case 4:
                    self.frames[i].place(x=190, y=y)
                case _:
                    self.frames[i].place(x=70, y=y)
        