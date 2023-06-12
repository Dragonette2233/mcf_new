import tkinter as tk
from playsound import playsound
import time
import os
import subprocess
from modules import mcf_styles
from mcf_data import currentGameData
from mcf_threads import MCFThread
from mcf_riot_api import (
    RiotAPI,  
    MCFNoConnectionError,
    MCFTimeoutError
)
from mcf_data import (
    REGIONS_TUPLE,
    currentGameData,
    ALL_CHAMPIONS_IDs,
    PAPICH_SONG_PATH,
    SPECTATOR_FILE_PATH,
    SPECTATOR_MODE,
    MCFStorage,
    Switches
)


class MCF_Gamechecker:
    def __init__(self, master) -> None:
        self.parent = master
        self.entry = mcf_styles.Entry(width=19)
        self.endtime = mcf_styles.Label(fsize=9)
        self.characters = [tk.Label(master, borderwidth=0) for _ in range(0, 10)]
        self.win = mcf_styles.Label(fsize=26, height=3, width=14, hlb='#370d3d')
        self.lastgame = mcf_styles.Label(fsize=9, hlb='#370d3d', width=8)
        self.run_button = mcf_styles.Button(display=master.button_images['Run'],
                                            command=lambda: MCFThread(
                                                    func=self.awaiting_game_end
                                            ).start())
        self.specated_button = mcf_styles.Button(display=master.button_images['Spec'],
                                                 command=self.specate_active_game)
        self.search_button = mcf_styles.Button(display=master.button_images['Search'],
                                               command=lambda: MCFThread(
                                                    func=self.search_for_game
                                               ).start())
        self.arrow_button = mcf_styles.Button(display=master.button_images['Arrow'],
                                              command=self.restore_nickname_for_search)

        self.entry.place(in_=master, x=11, y=343)
        self.search_button.place(in_=master, x=11, y=370)
        self.arrow_button.place(in_=master, x=120, y=370)

    # Decorator for handling connection in methods
    def connection_handler(func):
        def wrapper(self, *args, **kwargs):
            
            Switches.decorator = True
            while Switches.decorator:
                try:
                    func(self, *args, **kwargs)
                    Switches.decorator = False
                except (MCFNoConnectionError, MCFTimeoutError) as ex:
                    self.parent.info_view.display_info(text=str(ex) + ' | Press refresh to stop', ground='red', delay=2)
                    time.sleep(2.5)
                    # func(self, *args, **kwargs)
            
        return wrapper
                
    # Decorator for disabling buttons for secure threading
    def disable_while_running(func):
        def wrapper(self, *args, **kwargs):
            self.search_button['state'] = 'disabled'
            self.run_button['state'] = 'disabled'
            self.arrow_button['state'] = 'disabled'
            func(self, *args, **kwargs)
            self.search_button['state'] = 'normal'
            self.run_button['state'] = 'normal'
            self.arrow_button['state'] = 'normal'

        return wrapper
    
    def _refresh(self):

        for widget in *self.characters, self.specated_button, self.run_button, \
                       self.endtime, self.win, self.lastgame:
            widget.place_forget()
        
        self.entry.delete(0, 'end')

    def restore_nickname_for_search(self):

        stored_nickname = MCFStorage.get_selective_data(route=('CheckerLast',))
        self.entry.insert(0, stored_nickname)

    @connection_handler
    @disable_while_running
    def search_for_game(self):

        currentGameData.region, currentGameData.area = None, None
        summoner_name = self.entry.get().split(':')
        self.endtime.place_forget()
        self.lastgame.place_forget()
        
        if len(summoner_name) != 2:
            self.parent.info_view.display_info(text='Use ":"', ground='red', delay=3)
            return
        
        for short, code, area in REGIONS_TUPLE:
            if summoner_name[1].lower() == short:
                currentGameData.region = code
                currentGameData.area = area
                break

        if currentGameData.region is None:
            self.parent.info_view.display_info(text='Wrong region', ground='red', delay=1.75)
            return
        
        self.parent.info_view.display_info(text='Searching', ground='yellow')
    
        summoner_name = RiotAPI.get_summoner_by_name(region=currentGameData.region, name=summoner_name[0])
        
        if summoner_name.get('status'):
            self.parent.info_view.display_info(text='Summoner not found', ground='red', delay=1.75)
            return
        
        currentGameData.summoner_puuid = summoner_name['puuid']
        response_activegame = RiotAPI.get_active_by_summonerid(region=currentGameData.region, 
                                                               summid=summoner_name['id'],
                                                               status=True)
            
        # Writing nick and region to json
        MCFStorage.write_data(route=('CheckerLast',), value=self.entry.get())
        
        if response_activegame.status_code != 200:
            self.parent.info_view.display_info(text='Loading last game')
            self.show_lastgame_info()
        else:
        
            '''Запрос активной игры'''

            currentGameData.response = response_activegame.json()
            currentGameData.game_id = str(currentGameData.response['gameId']) # 1237890
            currentGameData.match_id = currentGameData.region.upper() + '_' + currentGameData.game_id # EUW_12378912
            currentGameData.players_count = currentGameData.response['participants'] # [0] {}, [1] {}, 2 {}, ... [10] {}
            self.show_character_icons()
            
            self.specated_button.place(x=427, y=342)
            self.run_button.place(x=427, y=296)
            self.parent.info_view.hide_info()
        # canvas.info_manager(forget=True)
    
    def show_character_icons(self, activegame=True):
        global cnv_images, canvas

        characters_name = []
        # players_count = currentGameData.response['participants']
        
        if len(currentGameData.players_count) == 10:
            print('Ten players')
            
            for p in range(0, 10):
                champ_name = ALL_CHAMPIONS_IDs.get(currentGameData.players_count[p]['championId'])
                self.characters[p]['image'] = self.parent.character_icons[champ_name]
                characters_name.append(champ_name)
            for i, x in zip(range(5), (168, 210, 252, 294, 336)):
                self.characters[i].place(x=x, y=300)
            
            for i, x in zip(range(5, 10), (185, 227, 269, 311, 353 )):
                self.characters[i].place(x=x, y=367)
        
        # Inserting names in stats entries
        if activegame:
            self.parent.obj_aram.refill_characters_entrys(
                blue_chars = ' '.join(characters_name[0:5]),
                red_chars = ' '.join(characters_name[5:10])
            )
            MCFStorage.write_data(route=('Stats', ),
                                  value={
                                      'T1': ' '.join(characters_name[0:5]),
                                      'T2': ' '.join(characters_name[5:10])
                                  })
                                  
            # if Switches.elorank:
            #     cnv_images['elocanvas'] = canvas.create_image(383, 345, image=cnv_images['eloimage'], anchor=tk.NW)
    
    def specate_active_game(self):
        list_task = os.popen('tasklist /FI "IMAGENAME eq League of Legends*"').readlines()
        
        if len(list_task) != 1:
            self.parent.info_view.display_info(text='Game already running', ground='red', delay=1.75)
            return
        
        self.parent.info_view.display_info(text='Launching spectator..', delay=1.75)

        enc_key = currentGameData.response['observers']['encryptionKey']
        spectator = SPECTATOR_MODE.format(reg=currentGameData.region)
        args = spectator, enc_key, str(currentGameData.game_id), currentGameData.region.upper()

        MCFStorage.write_data(route=("0", ), value=str(args))

        subprocess.call([SPECTATOR_FILE_PATH, *args])

    @connection_handler
    @disable_while_running
    def awaiting_game_end(self):
    # global sw_switches
        Switches.request = True
        self.parent.canvas.start_circle()
        self.parent.info_view.display_info(text='Matcher checker started', ground='#25D500', delay=1.5)

        while Switches.request:

            
            finished_game = RiotAPI.get_match_by_gameid(area=currentGameData.area, 
                                                        gameid=currentGameData.match_id, 
                                                        status=True)
            
                
            if finished_game.status_code == 200:

                response = finished_game.json()
                kills = sum(response['info']['participants'][k]['kills'] for k in range(10))
                time_stamp = list(divmod(response['info']['gameDuration'], 60))

                # for k in range(0, 10): kills += int(response['info']['participants'][k]['kills'])
                if time_stamp[1] < 10: 
                    time_stamp[1] = f"0{time_stamp[1]}"

                if response['info']['teams'][0]['win']: 
                    team = ('blue', '1')
                else: 
                    team = ('red', '2')

                self.win['text'] = f"{team[0].upper()} SIDE (П{team[1]})\n|  {kills}  |"
                self.win['bg'] = team[0]
                self.endtime['text'] = f" {time_stamp[0]}:{time_stamp[1]} "
                self.endtime['highlightbackground'] = team[0]

                # switchAppAndGhostView(minimize=False)
                self.endtime.place(x=223, y=275)
                self.win.place(x=92, y=143)
                self.specated_button.place_forget()
                self.run_button.place_forget()
                Switches.request = False
                playsound(PAPICH_SONG_PATH)
                finished_game.close()
            
            time.sleep(2.2)

    @connection_handler
    def show_lastgame_info(self):
        
        games_list = RiotAPI.get_matches_by_puuid(area=currentGameData.area, 
                                                  puuid=currentGameData.summoner_puuid)
        
        if len(games_list) == 0:

            self.parent.info_view.display_info(text='No games for this summoner', ground='red', delay=1.5)
            return

        lastgame = RiotAPI.get_match_by_gameid(area=currentGameData.area, gameid=games_list[0])
        
        currentGameData.players_count = lastgame['info']['participants'] # [0] {}, [1] {}, 2 {}, ... [10] {}
        currentGameData.teams_info = lastgame['info']['teams'] # [0] {}, [1] .
        
        if len(currentGameData.players_count) < 10:
            self.parent.info_view.display_info(text='Corrupted data or very old', ground='red', delay=1.5)
            return
        
        self.show_character_icons(activegame=False)
        kills = sum(currentGameData.players_count[k]['kills'] for k in range(10))
        # print(currentGameData.players_count.keys())
        if currentGameData.teams_info[0]['win']:
            text, color = f' W1 | {kills} ', 'blue'
        else:
            text, color = f' W2 | {kills} ', 'red'
            
        timestamp = list(divmod(lastgame['info']['gameDuration'], 60))
        if timestamp[1] < 10:
            timestamp[1] = f"0{timestamp[1]}"
        
        self.endtime.configure(
                text=f"  {timestamp[0]}:{timestamp[1]}  ",
                highlightbackground=color
            )
        
        self.lastgame.configure(
                text=text, # bg=color
                highlightbackground=color
            )

        self.lastgame.place(x=183, y=342)
        self.endtime.place(x=309, y=342)
        self.parent.info_view.hide_info()