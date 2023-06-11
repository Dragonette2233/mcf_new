import sys
import requests
import json
from bs4 import BeautifulSoup as bs
from mcf_data import ALL_CHAMPIONS_IDs
import threading

class MCFTimeoutError():
    def __repr__(self) -> str:
        return 'Error: Timeout'

class MCFNoConnectionError():
    def __repr__(self) -> str:
        return 'Error: Connection lost'

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
    def get_api(cls):
        return cls.__api_key

    @staticmethod
    def connection_handler(func):
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
            except requests.exceptions.ConnectTimeout:
                result = MCFTimeoutError()
            except Exception:
                result = MCFNoConnectionError()
            return result
        return wrapper

    @connection_handler
    @staticmethod
    def get_summoner_by_name(region: str, name: str, puuid=False) -> dict:
        result = requests.get(RiotAPI.__link_summoner_by_name.format(region=region, name=name), **RiotAPI.__headers_timeout)
        
        if puuid:
            return result.json()['puuid']
        
        return result.json()
    
    @connection_handler
    @staticmethod
    def get_matches_by_puuid(area: str, puuid: int):
        result = requests.get(RiotAPI.__link_matches_by_puuid.format(area=area, puuid=puuid), **RiotAPI.__headers_timeout)

        return result.json()
    
    @connection_handler
    @staticmethod
    def get_match_by_gameid(area: str, gameid: int, status=False):
        result = requests.get(RiotAPI.__link_match_by_gameid.format(area=area, gameid=gameid), **RiotAPI.__headers_timeout)
        
        if status:
            return result
        return result.json()
    
    @connection_handler
    @staticmethod
    def get_active_by_summonerid(region: str, summid: int, status=False):
        result = requests.get(RiotAPI.__link_active_by_summid.format(region=region, summid=summid), **RiotAPI.__headers_timeout)
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
    @staticmethod
    def get_poro_games(red_champion: str = None, gamemode: str = None):

        if red_champion.title() not in ALL_CHAMPIONS_IDs.values():
            print('This champion unaccesible')
            return
        
        match gamemode:
            case 'aram':
                url = PoroAPI.__link_aram.format(champion=red_champion)
            case 'ranked-flex':
                url = PoroAPI.__link_rnk_flex.format(champion=red_champion)
            case 'ranked-solo':
                url = PoroAPI.__link_rnk_solo.format(champion=red_champion)
            case _:
                print('This gamemode unaccesible')
                return

        result = requests.get(url, **PoroAPI.__headers_timeout)
        soup: bs = bs(result.text, "html.parser").find_all('div', class_='cardTeam')
        
        games = {
            'teams': [team.find_all('img') for i, team in enumerate(soup) if i % 2 == 0],
            'champions': [],
            'nicknames': [team.find('div', class_='name').text.strip() for i, team in enumerate(soup) if i % 2 == 0],
            'regions': [team.find('a', class_='liveGameLink').get('href') for i, team in enumerate(soup) if i % 2 == 0],
            'elorank': [team.find('div', class_='subname').text.strip() for i, team in enumerate(soup) if i % 2 == 0]
        }

        for game in games['teams']:
            
            ids = [int(str(ids.get('class')).split('-')[1]) for ids in game[0:5]]
            converted_ids = [ALL_CHAMPIONS_IDs.get(i) for i in ids]
            games['champions'].append(converted_ids)

        with open('.\mcf_lib\GamesPoro.json', 'r', encoding='utf-8') as json_executable:
            json_object = json.load(json_executable)
            json_object[gamemode].clear()
        
        for c, n, r, e in zip(games['champions'], games['nicknames'], games['regions'], games['elorank']):
            json_object[gamemode].append(f"{' | '.join(c)}-|-{n}:{r.split('/')[2].upper()}:{e}")

        with open('.\mcf_lib\GamesPoro.json', 'w+', encoding='utf-8') as json_generated:
             json.dump(json_object, json_generated, indent=4)
        
        return 0
        
        
if __name__ == '__main__':
    PoroAPI.get_poro_games(red_champion=sys.argv[2], gamemode=sys.argv[3])
    
