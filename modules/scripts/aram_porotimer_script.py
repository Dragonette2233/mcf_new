from bs4 import BeautifulSoup as bs
import time
import requests
from mcf_data import cookies, headers
from mcf_data import Switches

def start_timer():

    link = 'https://lite.1xbet-new.com/ru/live/cyber-zone/league-of-legends'

    while Switches.timer:
        
        time.sleep(4)
        resp = requests.get(link, cookies=cookies, headers=headers)
        soup = bs(resp.text, 'html.parser')
        games_list = soup.find_all('ul', class_='dashboard-champs-list')
        gamemodes = [game.find_all('span', class_='caption__label') for game in games_list]

        possible_game: str = gamemodes[0][0].text.strip()
        possible_link: str = gamemodes[0][0]

        if possible_game.startswith('All'):
            # print('ARAM finded')
            game_route = gamemodes[0][0].find('a').get('href')

            new_link = 'https://lite.1xbet-new.com' + game_route
            new_resp = requests.get(new_link, cookies=cookies, headers=headers)

            new_bs = bs(new_resp.text, 'html.parser')
            gametime = new_bs.find('span', class_='dashboard-game-card__caption').text
            if gametime is not None:
                actual_time = gametime.strip().split(' / ')[0]
                minutes = actual_time.split(':')[0]

                if minutes in ('00', '01', '02', '03', '04', '05', '06'):
                    print('Game Started')
                    # app.info('Game started') -- Teemo song
                    break
                else:
                    print('Still waiting')
            else:
                print('Still waiting')
        else:
            print('Still waiting')
    