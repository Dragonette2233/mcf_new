import os
import json

"""
    Values for interacting with League of Legends data

"""
ALL_CHAMPIONS_IDs = {
    1: 'Annie', 2: 'Olaf', 3: 'Galio', 4: 'TwistedFate',
    5: 'XinZhao', 6: 'Urgot', 7: 'LeBlanc', 8: 'Vladimir',
    9: 'Fiddlesticks', 10: 'Kayle', 11: 'MasterYi',
    12: 'Alistar', 13: 'Ryze', 14: 'Sion', 15: 'Sivir',
    16: 'Soraka', 17: 'Teemo', 18: 'Tristana', 19: 'Warwick',
    20: 'Nunu', 21: 'MissFortune', 22: 'Ashe', 23: 'Tryndamere',
    24: 'Jax', 25: 'Morgana', 26: 'Zilean', 27: 'Singed',
    28: 'Evelynn', 29: 'Twitch', 30: 'Karthus', 31: "ChoGath",
    32: 'Amumu', 33: 'Rammus', 34: 'Anivia', 35: 'Shaco',
    36: 'DrMundo', 37: 'Sona', 38: 'Kassadin', 39: 'Irelia', 
    40: 'Janna', 41: 'Gangplank', 42: 'Corki', 43: 'Karma',
    44: 'Taric', 45: 'Veigar', 48: 'Trundle', 50: 'Swain',
    51: 'Caitlyn', 53: 'Blitzcrank', 54: 'Malphite', 55: 'Katarina', 
    56: 'Nocturne', 57: 'Maokai', 58: 'Renekton', 59: 'JarvanIV', 
    60: 'Elise', 61: 'Orianna', 62: 'Wukong', 63: 'Brand',
    64: 'LeeSin', 67: 'Vayne', 68: 'Rumble', 69: 'Cassiopeia',
    72: 'Skarner', 74: 'Heimerdinger', 75: 'Nasus', 76: 'Nidalee',
    77: 'Udyr', 78: 'Poppy', 79: 'Gragas', 80: 'Pantheon',
    81: 'Ezreal', 82: 'Mordekaiser', 83: 'Yorick', 84: 'Akali',
    85: 'Kennen', 86: 'Garen', 89: 'Leona', 90: 'Malzahar',
    91: 'Talon', 92: 'Riven', 96: "KogMaw", 98: 'Shen',
    99: 'Lux', 101: 'Xerath', 102: 'Shyvana', 103: 'Ahri',
    104: 'Graves', 105: 'Fizz', 106: 'Volibear', 107: 'Rengar',
    110: 'Varus', 111: 'Nautilus', 112: 'Viktor', 113: 'Sejuani',
    114: 'Fiora', 115: 'Ziggs', 117: 'Lulu', 119: 'Draven',
    120: 'Hecarim', 121: "KhaZix", 122: 'Darius', 126: 'Jayce',
    127: 'Lissandra', 131: 'Diana', 133: 'Quinn', 134: 'Syndra',
    136: 'AurelionSol', 141: 'Kayn', 142: 'Zoe', 143: 'Zyra',
    145: "KaiSa", 147: "Seraphine", 150: 'Gnar', 154: 'Zac',
    157: 'Yasuo', 161: "VelKoz", 163: 'Taliyah', 166: "Akshan",
    164: 'Camille', 200: "BelVeth", 201: 'Braum', 202: 'Jhin',
    203: 'Kindred', 221: 'Zeri', 222: 'Jinx', 223: "TahmKench", 233: "Briar",
    234: 'Viego', 235: 'Senna', 236: 'Lucian', 238: 'Zed',
    240: 'Kled', 245: 'Ekko', 246: 'Qiyana', 254: 'Violet',
    266: 'Aatrox', 267: 'Nami', 268: 'Azir', 350: 'Yuumi',
    360: 'Samira', 412: 'Thresh', 420: 'Illaoi', 421: "RekSai",
    427: 'Ivern', 429: 'Kalista', 432: 'Bard', 497: 'Rakan',
    498: 'Xayah', 516: 'Ornn', 517: 'Sylas', 526: 'Rell',
    518: 'Neeko', 523: 'Aphelios', 555: 'Pyke', 875: "Sett",
    711: "Vex", 777: "Yone", 887: "Gwen", 876: "Lillia",
    888: "Renata", 895: "Nilah", 897: "KSante", 902: "Milio", 950: "Naafiri", 
    2002: 'Kayn_b', 910: "Hwei",
    2001: "MonkeyKing"
}

eight_roles_dict = {

    '1': ('Aatrox', 'Belveth', 'Camille', 'Darius', 'Fiora', 'Gnar', 'Gwen', 'Illaoi', 'Irelia', 'Kayn', 
                    'Leesin', 'Renekton', 'Viego', 'Sylas', 'Sett', 'Swain', 'Hecarim', 'Mordekaiser', 'Tryndamere', 
                    'Riven', 'Nasus', 'Jax', 'Yasuo', 'Yone', 'Olaf','Violet', 'Wukong', 'Xinzhao', 'Trundle', 'Kled',
                    'Monkeyking', 'Graves', 'Naafiri'),
    '2': ('Akali', 'Kassadin', 'Masteryi', 'Rengar', 'Khazix', 'Evelynn', 'Talon', 'Zed', 'Leblanc', 'Nocturne', 
                 'Qiyana', 'Katarina', 'Pyke', 'Briar'),
    '3': ('Azir', 'Cassiopeia', 'Lillia', 'Ryze', 'Viktor',  'Ekko', 'Gangplank', 'Anivia', 'Heimerdinger', 
                    'Vladimir', 'Fiddlesticks', 'Kennen',  'Aurelionsol', 'Gragas', 'Ahri', 'Hwei'),
    '4': ('Bard', 'Janna', 'Karma', 'Lulu', 'Maokai', 'Morgana', 'Nami', 'Orianna', 'Rakan', 'Renata', 'Senna', 
                 'Seraphine', 'Sona', 'Soraka', 'Twistedfate', 'Yuumi', 'Zilean', 'Ivern',  'Yorick', 'Annie', 'Milio'),
    '5': ('Akshan', 'Aphelios', 'Caitlyn', 'Ezreal', 'Jhin', 'Jinx', 'Kaisa', 'Kalista', 'Kayle', 'Kindred', 
                   'Kogmaw', 'Lucian', 'Missfortune', 'Samira', 'Sivir', 'Tristana', 'Twitch', 'Vayne', 'Xayah', 
                   'Zeri', 'Draven', 'Quinn', 'Nilah'),
    '6':('Syndra', 'Velkoz', 'Xerath', 'Ziggs', 'Zoe', 'Corki', 'Ashe', 'Karthus', 'Malzahar', 'Lux', 'Zyra',
                    'Brand', 'Taliyah', 'Vex', 'Shaco', 'Teemo',),
    '7': ('Fizz',  'Lissandra', 'Nidalee', 'Neeko', 'Nunu', 'Varus', 'Veigar', 'Pantheon', 'Rumble', 'Shyvana',  
              'Reksai', 'Diana', 'Jayce', 'Elise', 'Malphite',),
   '8': ('Alistar', 'Amumu', 'Braum', 'Chogath', 'Drmundo', 'Galio', 'Garen',  'Leona', 'Nautilus', 'Ornn',
             'Poppy', 'Rammus', 'Rell', 'Sejuani', 'Shen', 'Sion', 'Skarner', 'Tahmkench', 'Taric', 'Thresh', 'Udyr', 
             'Urgot', 'Volibear', 'Warwick', 'Zac', 'Blitzcrank', 'Singed', 'Jarvaniv', 'Ksante')

}

ten_roles_dict = {

    '0': ('Aatrox', 'Belveth', 'Camille', 'Darius', 'Fiora', 'Gwen', 'Illaoi', 'Irelia', 'Kayn', 
           'Leesin', 'Renekton', 'Viego', 'Sett', 'Hecarim', 'Mordekaiser', 'Riven', 'Violet', # Vi is Violet
           'Kled', 'Warwick', 'Naafiri'),
    '1': ('Swain', 'Sylas', 'Jax', 'Yone', 'Yasuo', 'Trundle', 'Xinzhao', 'Graves', 'Monkeyking',
           'Tryndamere', 'Gnar', 'Wukong', 'Olaf', 'Nasus'),
    '2': ('Akali', 'Kassadin', 'Masteryi', 'Rengar', 'Khazix', 'Evelynn', 'Talon', 'Zed', 'Nocturne',
           'Qiyana', 'Katarina', 'Pyke', 'Samira', 'Briar'),
    '3': ('Azir', 'Cassiopeia', 'Lillia', 'Ryze', 'Viktor',  'Ekko', 'Gangplank', 'Anivia', 'Heimerdinger', 
           'Vladimir', 'Fiddlesticks', 'Kennen',  'Aurelionsol', 'Gragas', 'Ahri', 'Hwei'),
    '4': ('Bard', 'Janna', 'Karma', 'Lulu', 'Maokai', 'Morgana', 'Nami', 'Orianna', 'Rakan', 'Renata', 'Senna', 
           'Seraphine', 'Sona', 'Soraka', 'Twistedfate', 'Yuumi', 'Zilean', 'Ivern',  'Yorick', 'Annie', 'Milio'),
    '5': ('Akshan', 'Aphelios', 'Caitlyn', 'Jhin', 'Jinx', 'Kaisa', 'Kalista', 'Kayle', 'Kindred', 
           'Kogmaw', 'Lucian', 'Missfortune', 'Sivir', 'Tristana', 'Twitch', 'Vayne', 'Xayah', 
           'Zeri', 'Draven', 'Quinn', 'Nilah'),
    '6':('Syndra', 'Velkoz', 'Xerath', 'Ziggs', 'Zoe', 'Corki', 'Ashe', 'Karthus', 'Malzahar', 'Lux', 'Zyra',
          'Brand', 'Taliyah', 'Vex', 'Shaco', 'Teemo',),
    '7': ('Lissandra', 'Nidalee', 'Neeko', 'Nunu', 'Varus', 'Veigar', 'Pantheon', 'Rumble', 'Shyvana',  
           'Reksai', 'Diana', 'Jayce', 'Elise', 'Malphite', 'Leblanc', 'Jarvaniv', 'Fizz', 'Ezreal',),
    '8': ('Drmundo', 'Galio', 'Garen', 'Ornn', 'Poppy', 'Sion', 'Udyr', 'Ksante', 'Singed',
           'Urgot', 'Volibear'),
    '9': ('Alistar', 'Amumu', 'Braum', 'Leona', 'Nautilus', 'Shen', 'Tahmkench', 'Thresh', 'Skarner',
           'Zac', 'Blitzcrank', 'Rammus', 'Sejuani', 'Chogath', 'Rell', 'Taric')

}

APP_TITLE = 'mcf_development'
ELO_SYMBOLS = ('BR', 'CH', 'DI', 'GO', 'GR', 'IR', 'MA', 'PL', 'PP', 'SI', 'UN')
SPECTATOR_MODE = 'spectator.{reg}.lol.pvp.net:8080'
FEATURED_GAMES_URL = "https://{region}.api.riotgames.com/lol/spectator/v4/featured-games"
URL_PORO_BY_REGIONS = "https://porofessor.gg/current-games/{champion}/{region}/queue-450"
REGIONS_TUPLE = (
    ('br', 'br1', 'americas'), ('lan', 'la1', 'americas'),
    ('na', 'na1', 'americas'), ('las', 'la2', 'americas'),
    ('oce', 'oc1', 'sea'), ('eune', 'eun1', 'europe'),
    ('tr', 'tr1', 'europe'), ('ru', 'ru', 'europe'),
    ('euw', 'euw1', 'europe'), ('kr', 'kr', 'asia'), 
    ('jp', 'jp1', 'asia'), ('vn', 'vn2', 'sea'),
    ('sg', 'sg2', 'sea'), ('ph', 'ph2', 'sea'),
    ('th', 'th2', 'sea'), ('tw', 'tw2', 'sea')
)

"""
    All pathes for app images
    
"""

MCF_ROOT_PATH = os.environ.get('MCF_ROOT')
BUTTONS_PATH = os.path.join(MCF_ROOT_PATH, 'images_lib', 'buttons/')
APP_ICON_PATH = os.path.join(MCF_ROOT_PATH, 'images_lib', 'backgrounds', 'icon_f.png')
BACKGROUND_IMAGES_PATH = os.path.join(MCF_ROOT_PATH, 'images_lib', 'backgrounds')
CHARARACTER_ICON_PATH = os.path.join(MCF_ROOT_PATH, 'images_lib', 'chars', 'display_icons')
LOADING_STOP_PATH = os.path.join(MCF_ROOT_PATH, 'images_lib', 'loading_gif', 'load_end.png')
LOADING_START_PATH = os.path.join(MCF_ROOT_PATH, 'images_lib', 'loading_gif', 'load_{index}.png')
JSON_GAMEDATA_PATH = os.path.join(MCF_ROOT_PATH, 'mcf_lib', 'GameData.json')
PAPICH_SONG_PATH = os.path.join(MCF_ROOT_PATH, 'mcf_lib', 'song.mp3')
SCREEN_GAMESCORE_PATH = os.path.join(MCF_ROOT_PATH, 'images_lib', 'gamescore_PIL.png')
TEEMO_SONG_PATH = os.path.join(MCF_ROOT_PATH, 'mcf_lib', 'hihi.mp3')
SPECTATOR_FILE_PATH = os.path.join(MCF_ROOT_PATH, 'mcf_lib', 'spectate.bat')
SCREENSHOT_FILE_PATH = os.path.join(MCF_ROOT_PATH, 'images_lib', 'screenshot_PIL.png')


"""
    Data for screen score recognizing (Time, kills, towers)

"""

GTIME_DATA_PATH = os.path.join(MCF_ROOT_PATH, 'ssim_score_data', 'gametime')
BLUE_SCORE_PATH = os.path.join(MCF_ROOT_PATH, 'ssim_score_data', 'team_blue', 'score_{pos}')
RED_SCORE_PATH =  os.path.join(MCF_ROOT_PATH, 'ssim_score_data', 'team_red', 'score_{pos}')
BLUE_TOWER_PATH = os.path.join(MCF_ROOT_PATH, 'ssim_score_data', 'team_blue', 'towers')
RED_TOWER_PATH = os.path.join(MCF_ROOT_PATH, 'ssim_score_data', 'team_red', 'towers')

DEBUG_STATS_PATH = os.path.join(MCF_ROOT_PATH, 'arambot_lib', 'debug_stats.json')

"""
    Classes for finded game and switches for controling threads and activity 

"""

class MCFException(Exception): ...
class MCFTimeoutError(Exception): ...
class MCFNoConnectionError(Exception): ...

class MCFStorage:

    @classmethod
    def save_score(cls, score: dict = None, stop_tracking=False):

        with open(os.path.join(MCF_ROOT_PATH, 'arambot_lib', 'activegame_score.json'), 'r') as file:
            data = json.load(file)

        if stop_tracking:
            data['is_active'] = False
        else:
            data = score
        
        with open(os.path.join(MCF_ROOT_PATH, 'arambot_lib', 'activegame_score.json'), 'w+') as file:
            json.dump(data, file, indent=4)

    @classmethod
    def get_selective_data(cls, route: tuple):
        data = json.load(open(JSON_GAMEDATA_PATH, 'r'))
        if isinstance(route, tuple):
            if len(route) > 1:
                return data[route[0]][route[1]]
            else:
                return data[route[0]]
        else:
            raise TypeError('Provide touple for executing MCFData')


    @classmethod
    def get_all_data(cls) -> dict:
        data = json.load(open(JSON_GAMEDATA_PATH, 'r'))
        return data

    @classmethod
    def write_data(cls, route: tuple, value):
        data = json.load(open(JSON_GAMEDATA_PATH, 'r'))
        if isinstance(route, tuple):
            if len(route) > 1:
                data[route[0]][route[1]] = value
            else:
                data[route[0]] = value
            json.dump(data, open(JSON_GAMEDATA_PATH, 'w+'), indent=4)
        else:
            raise TypeError('Provide touple for executing MCFData')
    
    @classmethod
    def stats_monitor(cls, validor):

        is_plus = True

        match list(validor.values()):
            case [_, __, 0, 0]:
                return
            case [1, 0, 1, 0]:
                is_plus = True
            case [0, 1, 0, 1]:
                is_plus = True
            case [0, 1, 1, 0]:
                is_plus = False
            case [1, 0, 0, 1]:
                is_plus = False
            case _:
                # print(list(Validator.stats_register.values()))
                print('UNDEFINED IN STATS MONITOR. CHECK CODE')
                return

        import json

        with open(DEBUG_STATS_PATH, 'r', encoding='utf-8') as js_stats:

            stats_register = json.load(js_stats)

        if is_plus:
            stats_register['PLUS'] += 1
        else:
            stats_register['minus'] += 1

        with open(DEBUG_STATS_PATH, 'w+', encoding='utf-8') as js_stats:

            json.dump(stats_register, js_stats, indent=4)


class CurrentGameData:
    response = None
    area = None
    region = None
    game_id = None
    match_id = None
    summoner_puuid = None
    teams_info = None
    champions_ids = None
    highlight_game = ''

    def __str__(self) -> str:
        return f"""
        response: {self.response}
        area: {self.area}
        region: {self.region}
        game_id: {self.game_id}
        match_id: {self.match_id}
        highlight_game: {self.highlight_game}
        """
    
    def reset(self):
        self.response = None
        self.area = None
        self.region = None
        self.game_id = None
        self.match_id = None
        self.summoner_puuid = None
        self.teams_info = None
        self.highlight_game = None

currentGameData = CurrentGameData()

# class Switch


class Validator:
    findgame = 0
    loop = False
    recognition = 0
    ended_game_characters = None
    finded_game_characerts = None
    stats_register = {
        'W1_res': 0,
        'W2_res': 0,
        'W1_pr': 0,
        'W2_pr': 0,
    }
    total_register = {
        'W1_res': 0,
        'W2_res': 0,
        'W1_pr': 0,
        'W2_pr': 0,
    }

class Switches:
    coeff_opened = False
    request = False
    after_info = None
    after_delay = None
    calibration_index = 0
    timer = None
    bot_activity = False
    predicted = False

cookies = {
        'auid': 'LY0LGGVJT9xF3cMHBakaAg==',
        'SESSION': '22fdb02ab99445348a011c35f47c6452',
        'lng': 'ru',
        '_cfvwab': '-1',
        'cookies_agree_type': '3',
        'tzo': '3',
        'is12h': '0',
        'che_g': '3c2afae5-894d-df7a-91d5-ba2642fb4db5',
        'sh.session.id': '798cfbe4-33cb-434c-affa-b0862a224c4f',
        '_ga': 'GA1.1.368426760.1699302170',
        '_ym_uid': '1699731283765603681',
        '_ym_d': '1699731283',
        '_ym_isad': '1',
        '_ga_7JGWL9SV66': 'GS1.1.1699729869.10.1.1699731302.34.0.0',
        'ggru': '188',
        'platform_type': 'mobile',
        '_ga_0NQW4X2MPH': 'GS1.1.1699731283.1.1.1699737050.59.0.0',
        'window_width': '802',
    }

headers = {
    'authority': 'lite.1xbet-new.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
}

poro_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36" }