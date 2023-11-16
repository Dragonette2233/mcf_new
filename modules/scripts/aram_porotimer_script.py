from bs4 import BeautifulSoup as bs
import time
import requests
from mcf_data import cookies, headers
from mcf_data import Switches


def start_timer():

    link = 'https://lite.1xbet-new.com/ru/live/cyber-zone/league-of-legends'

    try:
        resp = requests.get(link, cookies=cookies, headers=headers)
    except:
        return
    
    soup = bs(resp.text, 'html.parser')
    games_list = soup.find_all('ul', class_='dashboard-champs-list')
    gamemodes = [game.find_all('span', class_='caption__label') for game in games_list]

    try:
        possible_game: str = gamemodes[0][0].text.strip()
    except IndexError:
        return
    
    # possible_link: str = gamemodes[0][0]

    if possible_game.startswith('All'):
        try:
            game_route = gamemodes[0][0].find('a').get('href')
        except IndexError:
            return
        
        new_link = 'https://lite.1xbet-new.com' + game_route

        try:
            new_resp = requests.get(new_link, cookies=cookies, headers=headers)
        except:
            return

        new_bs = bs(new_resp.text, 'html.parser')

        try:
            gametime = new_bs.find('span', class_='dashboard-game-card__caption').text
        except:
            return

        if gametime is not None:
            actual_time = gametime.strip().split(' / ')[0]
            minutes = actual_time.split(':')[0]

            if minutes in ('00', '01', '02', '03', '04', '05', '06'):
                return str(actual_time)
            
    