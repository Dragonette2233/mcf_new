import sys
import requests
from bs4 import BeautifulSoup as bs
from mcf_data import (
    ALL_CHAMPIONS_IDs, 
    MCFStorage,
    MCFTimeoutError,
    MCFNoConnectionError,
    MCFException
)
# from mcf_build import MCFException
import logging
from pprint import pprint

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s\n',
    level=logging.ERROR,
    handlers=[
        logging.FileHandler('.\mcf_lib\mcf_logs.log'),
        logging.StreamHandler()
    ]
)


class TGApi:

    token = '6587599071:AAF_Wb0gAO7Zw_pS5hANgUfOBnVAR_mH60A'
    method_send = 'sendMessage'
    method_updates = 'getUpdates'
    tg_api_url = 'https://api.telegram.org/bot{token}/{method}'

    @classmethod
    def display_gamestart(cls, timer):

        requests.post(
            url=cls.tg_api_url.format(token=cls.token, method=cls.method_send),
            data={'chat_id': -4077907895, 'text': f'⚪️ Игра началась -- {timer}' }
        )

    @classmethod
    def winner_is(cls, team, kills):
        
        if team == 'blue':
            message = f'🔵 П1 -- {kills}'
        else:
            message = f'🔴 П2 -- {kills}'

        requests.post(
            url=cls.tg_api_url.format(token=cls.token, method=cls.method_send),
            data={'chat_id': -4077907895, 'text': message}
        )


class RiotAPI:
    if len(sys.argv) < 2:
        raise Exception('RiotAPI require API-key as argument for executing .py file')
    __api_key = sys.argv[1]
    __headers_timeout = {
        'headers': { "X-Riot-Token": __api_key },
        'timeout': 3
    }
    __link_summoner_by_name = "https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{name}"
    __link_matches_by_puuid = "https://{area}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=2"
    __link_match_by_gameid = "https://{area}.api.riotgames.com/lol/match/v5/matches/{gameid}"
    __link_active_by_summid = "https://{region}.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/{summid}"
    
    @classmethod
    def get_api_key(cls):
        return cls.__api_key
    
    @classmethod
    def get_headers_timeeout(cls):
        return cls.__headers_timeout

    @staticmethod
    def connection_handler(func):
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
            except (requests.exceptions.ConnectTimeout, 
                    requests.exceptions.ConnectionError):
                raise MCFException('No connection | Timeout')
            except MCFException as mcf_ex:
                raise MCFException(str(mcf_ex))
            except Exception as exc:
                logging.error(exc, exc_info=True)
                raise MCFException('Unknown error')
            return result
        return wrapper

    @connection_handler
    @staticmethod
    def get_summoner_by_name(region: str, name: str, puuid=False) -> dict:
        result = requests.get(RiotAPI.__link_summoner_by_name.format(region=region, name=name), 
                              **RiotAPI.__headers_timeout)
        
        if puuid:
            return result.json()['puuid']
        
        return result.json()
    
    @connection_handler
    @staticmethod
    def get_matches_by_puuid(area: str, puuid: int):
        result = requests.get(RiotAPI.__link_matches_by_puuid.format(area=area, puuid=puuid), 
                              **RiotAPI.__headers_timeout)

        return result.json()
    
    @connection_handler
    @staticmethod
    def get_match_by_gameid(area: str, gameid: int, status=False):
        result = requests.get(RiotAPI.__link_match_by_gameid.format(area=area, gameid=gameid), 
                              **RiotAPI.__headers_timeout)
        
        if status:
            return result
        return result.json()
    
    @connection_handler
    @staticmethod
    def get_active_by_summonerid(region: str, summid: int, status=False):
        result = requests.get(RiotAPI.__link_active_by_summid.format(region=region, summid=summid), 
                              **RiotAPI.__headers_timeout)
        if status:
            return result
        return result.json()
    
class PoroAPI:

    __headers_timeout = {
        'headers': { 
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36" },
        'timeout': 3
    }
    __link_rnk_solo = 'https://porofessor.gg/current-games/{champion}/queue-420'
    __link_rnk_flex = 'https://porofessor.gg/current-games/{champion}/queue-440'
    __link_aram = 'https://porofessor.gg/current-games/{champion}/queue-450'

    @RiotAPI.connection_handler
    @staticmethod
    def get_poro_games(red_champion: str = None, gamemode: str = None):
        """
            Avaliable gamemods: aram | ranked-flex | ranked-solo

        """

        if len(red_champion) < 2:
            raise MCFException('Short')

        converted_champion = None
        for champion in ALL_CHAMPIONS_IDs.values():
            if champion.capitalize().startswith(red_champion.capitalize()):
                converted_champion = champion.lower()
                break
        else:
            raise MCFException(f'Who is {red_champion}')
        
        match converted_champion:
            case 'wukong':
                converted_champion = 'monkeyking'
            case 'violet':
                converted_champion = 'vi'
            case _:
                pass

        match gamemode:
            case 'aram':
                url = PoroAPI.__link_aram.format(champion=converted_champion)
            case 'ranked-flex':
                url = PoroAPI.__link_rnk_flex.format(champion=converted_champion)
            case 'ranked-solo':
                url = PoroAPI.__link_rnk_solo.format(champion=converted_champion)
            case _:
                raise MCFException('This gamemod is unaccesible')
                
        result = requests.get(url, **PoroAPI.__headers_timeout)
        soup: bs = bs(result.text, "html.parser").find_all('div', class_='cardTeam')

        if result.status_code != 200:
            raise MCFException(f'Error. Status: {result.status_code}')
        
        games = {
            'teams': [team.find_all('img') for i, team in enumerate(soup) if i % 2 == 0],
            'champions': [],
            'nicknames': [team.find('div', class_='name').text.strip() for i, team in enumerate(soup) if i % 2 == 0],
            'regions': [team.find('a', class_='liveGameLink').get('href') for i, team in enumerate(soup) if i % 2 == 0],
            'elorank': [team.find('div', class_='subname').text.strip() for i, team in enumerate(soup) if i % 2 == 0]
        }

        for game in games['teams']:
            
            for i, champ in enumerate(game):
                if len(champ.get('class')) == 0:
                   del game[i]
            
            ids = [int(str(ids.get('class')).split('-')[1]) for ids in game[0:5]]
            converted_ids = [ALL_CHAMPIONS_IDs.get(i) for i in ids]
            games['champions'].append(converted_ids)

        featured_games = []
       

        for c, n, r in zip(games['champions'], games['nicknames'], games['regions']): # games['elorank']):
            featured_games.append(f"{' | '.join(c)}-|-{n}:{r.split('/')[2].upper()}")

        MCFStorage.write_data(route=('MatchesRift', ), value=featured_games)
      
        
        
if __name__ == '__main__':
    PoroAPI.get_poro_games(red_champion=sys.argv[2], gamemode=sys.argv[3])
    
