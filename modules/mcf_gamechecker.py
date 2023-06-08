import tkinter as tk
from modules import mcf_styles
from mcf_data import CurrentGameData
from mcf_riot_api import RiotAPI
from mcf_data import (
    REGIONS_TUPLE,
)

class MCF_Gamechecker:
    def __init__(self, master) -> None:
        self.entry = mcf_styles.Entry(width=19)
        self.endtime = mcf_styles.Label(fsize=9)
        self.characters = tuple(tk.Label(master, borderwidth=0) for _ in range(0, 10)),
        self.win = mcf_styles.Label(fsize=26, height=3, width=14, hlb='#370d3d')
        self.lastgame = mcf_styles.Label(fsize=9, hlb='#370d3d', width=8)
        self.run_button = mcf_styles.Button(display=master.button_images['Run'])
        self.specated_button = mcf_styles.Button(display=master.button_images['Spec'])
        self.search_button = mcf_styles.Button(display=master.button_images['Search'],
                                               command=self.search_for_game)
        self.arrow_button = mcf_styles.Button(display=master.button_images['Arrow'])
        
    def search_for_game(self):

        CurrentGameData.region, CurrentGameData.area = None, None
        summoner_name = self.entry.get().split(':')
        self.endtime.place_forget()
        self.lastgame.place_forget()
        
        if len(summoner_name) != 2:
            app_canvas.info_view.display_info(text='Hello', ground='red', delay=3)
            # showMainInfo(text='Use ":"', seconds=1.75, ground='red')
            print('Use ":"')
            return
        
        for short, code, area in REGIONS_TUPLE:
            if summoner_name[1].lower() == short:
                CurrentGameData.region = code
                CurrentGameData.area = area
                break

        if CurrentGameData.region is None:
            # showMainInfo(text='Wrong region', seconds=1.75, ground='red')
            print('Wrong Region')
            return
        
        # showMainInfo(text='Searching..')
        print('Searching')

        
        response_name = RiotAPI.get_summoner_by_name(region=CurrentGameData.region, name=summoner_name[0])

        if type(response_name) is str and response_name.startswith('Error |'):
            # showMainInfo(text=response_name, ground='red', seconds=1.5)
            print(response_name)
            return

        if response_name.get('status'):

            # showMainInfo(text='Summoner not found', seconds=1.75, ground='red')
            print('Summoner Not found')
            return
        
        response_activegame = RiotAPI.get_active_by_summonerid(region=CurrentGameData.region, summid=response_name['id'], status=True)
            
        if type(response_name) is str and response_name.startswith('Error |'):
            # showMainInfo(text='Timeout.. Try again', ground='red', seconds=1.5)
            return
        
        # Writing nick and region to json
        # getJsonData(key='CheckerLast', value=canvas.obj_match_c['entry'].get())

        if response_activegame.status_code != 200:
            # showMainInfo(text='Loading last game...')
            # showLastgameInfo(response_name)
            print('Not active')
            return
        
        '''Запрос активной игры'''

        CurrentGameData.response = response_activegame.json()
        CurrentGameData.game_id = str(CurrentGameData.response['gameId'])
        CurrentGameData.match_id = CurrentGameData.region.upper() + '_' + CurrentGameData.game_id
        # showCharactersIcons(CurrentGameData.response)

        self.specated_button.place(x=427, y=342)
        self.run_button.place(x=427, y=296)
        # canvas.info_manager(forget=True)

    