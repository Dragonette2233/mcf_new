from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from mcf_threads import MCFThread
from playsound import playsound
from mcf_data import (
    Switches,
    TEEMO_SONG_PATH
)
from mcf_riot_api import TGApi
import pyautogui
import time
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
            open_stream_source()

def aram_porotimer():
        from modules.scripts import aram_porotimer_script

        if not Switches.timer:

            Switches.timer = True
            app_blueprint.info_view._display_info('Waiting for ARAM...', 'blue')

            while Switches.timer:
                game = aram_porotimer_script.start_timer()
                if game is not None:
                    TGApi.display_gamestart(timer=game)
                    app_blueprint.info_view.notification(game)
                    playsound(TEEMO_SONG_PATH)
                    Switches.timer = False
                    
                    
                time.sleep(4)
            

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

    time.sleep(1.5)
    pyautogui.click(x=1897, y=97)
    time.sleep(4)
    pyautogui.click(x=1871, y=354)
    time.sleep(1.5)

    loop_validation = True
    
    while loop_validation:
        app_blueprint.obj_tophead.pillow_icons_recognition()
        team_blue = app_blueprint.obj_aram.blue_entry.get().split()
        team_red = app_blueprint.obj_aram.red_entry.get().split()

        if len(team_blue) < 4 and len(team_red) < 3:
            app_blueprint.info_view.exception('Recognizing Failed. Continue...')
            continue
        else:
            for char_b, char_r in zip(team_blue, team_red):
                try:
                    PoroAPI.get_poro_games(red_champion=char_r, gamemode='aram')
                    app_blueprint.obj_featured.parent.info_view.success('Done')

                except MCFException as ex:
                    app_blueprint.info_view.exception(str(ex))
                    break
                
                try:
                    games_by_character = storage_data.get_games_by_character(character=char_b, aram=False) # Characters-|-nickname:region
                    if games_by_character is not None:
                        for charlist in games_by_character:
                     
                            set_1 = set(team_blue)
                            set_2 = set(charlist.split('-|-')[0].split(' | '))
                            nickname = charlist.split('-|-')[1]

                            print(set_1)
                            print(set_2)
                            # Нахождение пересечения множеств
                            common_elements = set_1.intersection(set_2)

                            # Проверка наличия хотя бы трех общих элементов
                            if len(common_elements) >= 3:
                                print("Есть хотя бы три совпадающих элемента:", common_elements)
                                app_blueprint.obj_gamechecker.entry.delete(0, 'end')
                                app_blueprint.obj_gamechecker.entry.insert(0, nickname)
                                app_blueprint.obj_gamechecker.search_for_game()
                                # print(check_status)
                                if len(app_blueprint.obj_gamechecker.run_button.place_info()) != 0:
                                    app_blueprint.obj_gamechecker.awaiting_game_end()
                                    loop_validation = False
                                    break
                                break
                            else:
                                print("Недостаточно совпадающих элементов.")
                except MCFException as ex:
                    app_blueprint.info_view.exception(str(ex))
                    break
        
        time.sleep(3.5)
        # app_blueprint.info_view.success('Bot test success')

    driver.quit()