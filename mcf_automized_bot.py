from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from modules.scripts import async_poro_games
from mcf_threads import MCFThread
from playsound import playsound
from mcf_data import (
    Switches,
    TEEMO_SONG_PATH
)
from mcf_riot_api import TGApi
import pyautogui
import time
from pprint import pprint
from mcf_data import MCFException
from mcf_riot_api import PoroAPI
from mcf_build import MCFWindow
from modules.scripts import storage_data


app_blueprint = MCFWindow()


def run_autobot():

    if Switches.autobot is False:
        Switches.autobot = True
        while Switches.autobot:
            aram_porotimer()
            app_blueprint.refresh()
            open_stream_source()
            
    else:
        Switches.autobot = False
        Switches.loop_validator = False

def aram_porotimer():
        from modules.scripts import aram_porotimer_script

        if not Switches.timer:

            Switches.timer = True
            app_blueprint.info_view._display_info('Waiting for ARAM...', 'blue')

            while Switches.timer:
                game = aram_porotimer_script.start_timer()
                if game is not None:
                    if Switches.bot_activity:
                        TGApi.display_gamestart(timer=game)
                    app_blueprint.info_view.notification(game)
                    playsound(TEEMO_SONG_PATH)
                    Switches.timer = False
                    
                    
                time.sleep(4)

def run_autoscanner(driver: webdriver):

    # SEARCH_STATE = 'PORO' # Default: PORO. Could be switchet to API

    Switches.loop_validator = True
    while Switches.loop_validator:
        # print(len(app_blueprint.obj_aram.blue_entry.get()))
        if len(app_blueprint.obj_aram.blue_entry.get()) == 0:
            app_blueprint.obj_tophead.pillow_icons_recognition()
        team_blue = app_blueprint.obj_aram.blue_entry.get().split()
        team_red = app_blueprint.obj_aram.red_entry.get().split()

        if len(team_blue) < 4 or len(team_red) < 3:
            if Switches.recognition_validator == 27:
                Switches.recognition_validator = 0
                return 'FAIL'
            
            Switches.recognition_validator += 1
            app_blueprint.refresh()
            app_blueprint.info_view.exception('Recognizing Failed. Continue...')
            time.sleep(2)
            continue
        else:
            # print(len(team_blue), len(team_red))
            for char_b, char_r in zip(team_blue, team_red):

                try:
                    app_blueprint.info_view.notification('Parsing from RiotAPI and Poro...')

                    
                    async_poro_games.parse_games(champion_name=char_r) # Parse full PoroARAM by region
                    PoroAPI.get_poro_games(red_champion=char_r) # Parse only main page PoroARAM
                    app_blueprint.obj_featured.parse_aram_games() # Parse featured games from Riot API

                    app_blueprint.info_view.hide_info()
                except MCFException as ex:
                    app_blueprint.info_view.exception(str(ex))
                    break
                
                try:
                    games_by_character = storage_data.get_games_by_character(character=char_b, state='aram_poro')
                    games_by_character += storage_data.get_games_by_character(character=char_b, state='aram_poro_2')
                    games_by_character += storage_data.get_games_by_character(character=char_b, state='aram_api')

                    if games_by_character is not None:
                        for charlist in games_by_character:
                     
                            set_1 = set([i.lower().capitalize() for i in team_blue])
                            set_2 = set(charlist.split('-|-')[0].split(' | '))
                            set_2 = set([i.lower().capitalize() for i in set_2])

                            nicknames = charlist.split('-|-')[1].split('_|_')

                            # Нахождение пересечения множеств
                            common_elements = set_1.intersection(set_2)

                            # Проверка наличия хотя бы трех общих элементов
                            if len(common_elements) >= 4:
                                
                                for nick in nicknames:
                                    app_blueprint.obj_gamechecker.entry.delete(0, 'end')
                                    app_blueprint.obj_gamechecker.entry.insert(0, nick)
                                    app_blueprint.obj_gamechecker.search_for_game()
    
                                    if len(app_blueprint.obj_gamechecker.run_button.place_info()) != 0:
                                        pyautogui.click(x=1897, y=97)
                                        time.sleep(1.5)
                                        Switches.loop_validator = False
                                        MCFThread(func=app_blueprint.obj_gamechecker.awaiting_game_end, args=(driver, )).start()
                                        app_blueprint.obj_gamechecker.spectate_active_game()

                                        time.sleep(10)
                                        while Switches.request:
                                            time.sleep(4)
                                            app_blueprint.mcf_doubleclick(658, 1056)  
                                            app_blueprint.generate_score()
                                            
                                        app_blueprint.delete_screenscore()
                                        app_blueprint.close_league_of_legends()
                                        app_blueprint.info_view.notification('Porotimer starts in 4 mins.')
                                        time.sleep(240)
                                        # app_blueprint.obj_gamechecker.awaiting_game_end()
                                        return
                            else:
                                continue
                        else:
                            app_blueprint.info_view.notification(f'No games for {char_r} -- {char_b}. CD 3s')
                            Switches.try_validator += 1

                            if Switches.try_validator == 15:
                                Switches.try_validator = 0
                                return 'FAIL' 
                            time.sleep(3)
                    
                except MCFException as ex:
                    app_blueprint.info_view.exception(str(ex))
                    print(f'Autobot error: {ex}')
            
def open_stream_source():

    btn_stream = '//*[@id="app"]/div[3]/div/div/div[2]/main/div[2]/div/div/div[2]/div/ul/li/ul/li/div[1]/span[2]/span[2]/span/button'
    url = 'https://lite.1xbet-new.com/ru/live/cyber-zone/league-of-legends'

    driver = webdriver.Chrome()

    driver.maximize_window()

    # Открытие страницы
    driver.get(url)
    time.sleep(5)

    while True:
        try:
            element = WebDriverWait(driver, 4).until(
                EC.element_to_be_clickable((By.XPATH, btn_stream))
            )
            element.click()
            break
        except TimeoutException:
            app_blueprint.info_view.exception('No stream finded yet')
            continue

    # time.sleep(1.5)
    pyautogui.click(x=1897, y=97)
    time.sleep(9)
    pyautogui.click(x=1871, y=354)
    time.sleep(1.5)

    find_success = run_autoscanner(driver=driver)

    if find_success == 'FAIL':
        if Switches.bot_activity:
            TGApi.send_simple_message('Игра не найдена. Кулдаун 5 минут')
        time.sleep(300)

    driver.quit()