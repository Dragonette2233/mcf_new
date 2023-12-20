from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from modules.scripts import async_poro_games
from mcf_threads import MCFThread
from mcf_data import (
    Switches,
    Validator,
)
from mcf_riot_api import TGApi
import pyautogui
import time
from mcf_data import MCFException
from mcf_riot_api import PoroAPI
from mcf_build import MCFWindow
from modules.scripts import storage_data

class BetSite:
    xpath_btn_steam = '//*[@id="app"]/div[3]/div/div/div[2]/main/div[2]/div/div/div[2]/div/ul/li/ul/li/div[1]/span[2]/span[2]/span/button'
    css_btn_reject_live = 'button.ui-button.dashboard-redirect-message-timer__btn.ui-button--size-m.ui-button--theme-gray.ui-button--rounded'
    css_button_for_bet = 'li.ui-dashboard-champ.dashboard-champ.dashboard__champ.ui-dashboard-champ--theme-gray'
    css_table_games = 'li.ui-dashboard-champ.dashboard-champ.dashboard__champ.ui-dashboard-champ--theme-gray'
    main_url = 'https://lite.1xbet-new.com/ru/live/cyber-zone/league-of-legends'
    
    @classmethod
    def chrome_driver(cls):

        options = Options()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
        driver = webdriver.Chrome(options=options)
        driver.maximize_window()
        time.sleep(3)
        pyautogui.click(x=1896, y=99) #disable infobar
        return driver


    @classmethod
    def notify_when_starts(cls, driver: webdriver.Chrome):

        while True:
            # print('inloop')
            try:
                games = driver.find_elements(By.CSS_SELECTOR, 'li.ui-dashboard-champ.dashboard-champ.dashboard__champ.ui-dashboard-champ--theme-gray')
                aram_title_outer = games[0].find_element(By.CSS_SELECTOR, 'span.caption.ui-dashboard-champ-name__caption.caption--size-m')
                aram_title_inner: str = aram_title_outer.find_element(By.CSS_SELECTOR, 'span.caption__label').get_attribute('innerText')
              
                if aram_title_inner == 'All Random All Mid':
                    gametime_element = games[0].find_element(By.CSS_SELECTOR, 'span.dashboard-game-info__item.dashboard-game-info__time')
                    gametime = str(gametime_element.get_attribute('innerText'))

                    minutes = gametime.split(':')[0]

                    if minutes in ('00', '01', '02', '03', '04', '05', '09', '10'):
                        app_blueprint.info_view.notification(f'Game started: {gametime}')
                        TGApi.display_gamestart(timer=gametime)
                        return
                    else:
                        print(minutes)
                        time.sleep(1)
            except IndexError:
                # print(in_er)
                cls.remove_cancel(driver=driver)
                time.sleep(1)
            except (NoSuchElementException, StaleElementReferenceException):
                # print(bs_err)
                cls.remove_cancel(driver=driver)
                time.sleep(1)

    @classmethod
    def stream_activate(cls, driver: webdriver.Chrome):
        stream_active = 0
        while True:
            try:
                element = WebDriverWait(driver, 4).until(
                    EC.element_to_be_clickable((By.XPATH, cls.xpath_btn_steam))
                )
                element.click()
                return
            except (TimeoutException, NoSuchElementException):
                if stream_active == 20:
                    return 'FAIL'
                app_blueprint.info_view.exception('No stream finded yet')
                stream_active += 1
                continue

    @classmethod
    def stream_fullscreen(cls):
        time.sleep(6)
        pyautogui.click(x=1871, y=325)
        time.sleep(3.5)

    @classmethod
    def remove_cancel(cls, driver: webdriver.Chrome):

        try:
            element = driver.find_element(By.CSS_SELECTOR, cls.css_btn_reject_live)
            element.click()
        except NoSuchElementException:
            pass

    @classmethod
    def check_if_opened(cls, driver: webdriver.Chrome):
        for _ in range(120):
            try:
                games = driver.find_elements(By.CSS_SELECTOR, cls.css_table_games)
            except Exception as ex_:
                time.sleep(1)
                games = []
                print(ex_)
                
            try:
                button = games[0].find_element(By.CSS_SELECTOR, cls.css_button_for_bet)
                if not button.get_attribute('disabled'):
                    TGApi.send_simple_message('🟢Открыты')
                    break
            except NoSuchElementException:
                time.sleep(1)
                pass
            except IndexError:
                time.sleep(1)
                pass


app_blueprint = MCFWindow()


def run_autobot():

    driver = BetSite.chrome_driver()
    
    while True:
        app_blueprint.info_view.notification('Waiting for game')
        driver.get(BetSite.main_url)
        time.sleep(6)
        BetSite.remove_cancel(driver=driver)
        BetSite.notify_when_starts(driver=driver)
        stream_avaliable = BetSite.stream_activate(driver=driver)
        if stream_avaliable != 'FAIL':
            BetSite.stream_fullscreen()
            find_success = run_autoscanner(driver=driver)
            if find_success == 'FAIL':
                TGApi.send_simple_message('Игра не найдена. Кулдаун 5 минут')
                time.sleep(300)
        else:
            TGApi.send_simple_message('Кнопка стрима не активна. Кулдаун 5 минут')
            time.sleep(300)
        # open_stream_source(driver, BetSite.css_btn_reject_live, BetSite.xpath_btn_steam)
        


def run_autoscanner(driver: webdriver.Chrome):

    # SEARCH_STATE = 'PORO' # Default: PORO. Could be switchet to API

    Validator.loop = True
    while Validator.loop:
        # print(len(app_blueprint.obj_aram.blue_entry.get()))
        if len(app_blueprint.obj_aram.blue_entry.get()) == 0:
            app_blueprint.obj_tophead.pillow_icons_recognition()
        team_blue = app_blueprint.obj_aram.blue_entry.get().split()
        team_red = app_blueprint.obj_aram.red_entry.get().split()

        if len(team_blue) < 4 or len(team_red) < 3:
            if Validator.recognition == 40:
                Validator.recognition = 0
                return 'FAIL'
            
            Validator.recognition += 1
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
                                        pyautogui.click(x=1898, y=900)
                                        time.sleep(0.5)
                                        pyautogui.click(x=1898, y=1058)
                                        time.sleep(1.5)
                                        Validator.loop = False
                                        MCFThread(func=app_blueprint.obj_gamechecker.awaiting_game_end, args=(driver, )).start()
                                        app_blueprint.obj_gamechecker.spectate_active_game()

                                        time.sleep(10)
                                        while Switches.request:
                                            time.sleep(4)
                                            app_blueprint.mcf_doubleclick(658, 1056)  
                                            app_blueprint.generate_score()
                                            
                                        app_blueprint.delete_screenscore()
                                        app_blueprint.close_league_of_legends()
                                        app_blueprint.refresh()
                                        app_blueprint.info_view.notification('Porotimer starts in 4 mins.')
                                        if Switches.coeff_opened is False:
                                            MCFThread(func=BetSite.check_if_opened, args=(driver, )).start()
                                        
                                        Switches.coeff_opened = False
                                        time.sleep(240)
                                        # app_blueprint.obj_gamechecker.awaiting_game_end()
                                        return
                            else:
                                continue
                        else:
                            app_blueprint.info_view.notification(f'No games for {char_r} -- {char_b}. CD 3s')
                            Validator.findgame += 1

                            if Validator.findgame == 15:
                                Validator.findgame = 0
                                return 'FAIL' 
                            time.sleep(3)
                    
                except MCFException as ex:
                    app_blueprint.info_view.exception(str(ex))
                    print(f'Autobot error: {ex}')
            
def open_stream_source(driver: webdriver.Chrome):

    BetSite.remove_cancel(driver=driver)
    
    while True:
        try:
            games = driver.find_elements(By.CSS_SELECTOR, 'span.caption.ui-dashboard-champ-name__caption.caption--size-m')
            aram = games[0].get_attribute('innerText')

            if aram == 'All Random All Mid':
                gamearea = driver.find_elements(By.CSS_SELECTOR, 'li.ui-dashboard-champ.dashboard-champ.dashboard__champ.ui-dashboard-champ--theme-gray')
                gametime_element = gamearea[0].find_element(By.CSS_SELECTOR, 'span.dashboard-game-info__item.dashboard-game-info__time')
                gametime = str(gametime_element.get_attribute('innerText'))

                minutes = gametime.split(':')[0]

                if minutes in ('00', '01', '02', '03', '04', '05'):
                    app_blueprint.info_view.notification(f'Game started: {gametime}')
                    TGApi.display_gamestart(timer=gametime)
                    break
        except IndexError:
            BetSite.remove_cancel(driver=driver)
            time.sleep(1)
        except (NoSuchElementException, StaleElementReferenceException):
            BetSite.remove_cancel(driver=driver)
            time.sleep(1)

    stream_active = 0
    while True:
        try:
            element = WebDriverWait(driver, 4).until(
                EC.element_to_be_clickable((By.XPATH, BetSite.xpath_btn_steam))
            )
            element.click()
            break
        except (TimeoutException, NoSuchElementException):
            if stream_active == 20:
                break
            app_blueprint.info_view.exception('No stream finded yet')
            stream_active += 1
            continue

    # time.sleep(1.5)
    if stream_active != 20:

        time.sleep(6)
        pyautogui.click(x=1871, y=369)
        time.sleep(3.5)

        find_success = run_autoscanner(driver=driver)

        if find_success == 'FAIL':
            TGApi.send_simple_message('Игра не найдена. Кулдаун 5 минут')
            time.sleep(300)
    else:
        TGApi.send_simple_message('Кнопка стрима не активна. Кулдаун 5 минут')
        time.sleep(300)

    # driver.refresh()
    # time.sleep(6)