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
    203: 'Kindred', 221: 'Zeri', 222: 'Jinx', 223: "TahmKench",
    234: 'Viego', 235: 'Senna', 236: 'Lucian', 238: 'Zed',
    240: 'Kled', 245: 'Ekko', 246: 'Qiyana', 254: 'Violet',
    266: 'Aatrox', 267: 'Nami', 268: 'Azir', 350: 'Yuumi',
    360: 'Samira', 412: 'Thresh', 420: 'Illaoi', 421: "RekSai",
    427: 'Ivern', 429: 'Kalista', 432: 'Bard', 497: 'Rakan',
    498: 'Xayah', 516: 'Ornn', 517: 'Sylas', 526: 'Rell',
    518: 'Neeko', 523: 'Aphelios', 555: 'Pyke', 875: "Sett",
    711: "Vex", 777: "Yone", 887: "Gwen", 876: "Lillia",
    888: "Renata", 895: "Nilah", 897: "KSante", 902: "Milio", 2002: 'Kayn_b',
    2001: "MonkeyKing"
}

eight_roles_dict = {

    '1': ('Aatrox', 'Belveth', 'Camille', 'Darius', 'Fiora', 'Gnar', 'Gwen', 'Illaoi', 'Irelia', 'Kayn', 
                    'Leesin', 'Renekton', 'Viego', 'Sylas', 'Sett', 'Swain', 'Hecarim', 'Mordekaiser', 'Tryndamere', 
                    'Riven', 'Nasus', 'Jax', 'Yasuo', 'Yone', 'Olaf','Violet', 'Wukong', 'Xinzhao', 'Trundle', 'Kled',
                    'Monkeyking', 'Graves'),
    '2': ('Akali', 'Kassadin', 'Masteryi', 'Rengar', 'Khazix', 'Evelynn', 'Talon', 'Zed', 'Leblanc', 'Nocturne', 
                 'Qiyana', 'Katarina', 'Pyke'),
    '3': ('Azir', 'Cassiopeia', 'Lillia', 'Ryze', 'Viktor',  'Ekko', 'Gangplank', 'Anivia', 'Heimerdinger', 
                    'Vladimir', 'Fiddlesticks', 'Kennen',  'Aurelionsol', 'Gragas', 'Ahri'),
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
           'Kled', 'Warwick'),
    '1': ('Swain', 'Sylas', 'Jax', 'Yone', 'Yasuo', 'Trundle', 'Xinzhao', 'Graves', 'Monkeyking',
           'Tryndamere', 'Gnar', 'Wukong', 'Olaf', 'Nasus'),
    '2': ('Akali', 'Kassadin', 'Masteryi', 'Rengar', 'Khazix', 'Evelynn', 'Talon', 'Zed', 'Nocturne',
           'Qiyana', 'Katarina', 'Pyke', 'Samira'),
    '3': ('Azir', 'Cassiopeia', 'Lillia', 'Ryze', 'Viktor',  'Ekko', 'Gangplank', 'Anivia', 'Heimerdinger', 
           'Vladimir', 'Fiddlesticks', 'Kennen',  'Aurelionsol', 'Gragas', 'Ahri'),
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
SPECTATOR_MODE = 'spectator-consumer.{reg}.lol.pvp.net:80'
FEATURED_GAMES_URL = "https://{region}.api.riotgames.com/lol/spectator/v4/featured-games"
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

BUTTONS_PATH = os.path.join('.', 'images_lib', 'buttons/')
APP_ICON_PATH = os.path.join('.', 'images_lib', 'backgrounds', 'icon_f.png')
BACKGROUND_IMAGES_PATH = os.path.join('.', 'images_lib', 'backgrounds')
CHARARACTER_ICON_PATH = os.path.join('.', 'images_lib', 'chars', 'display_icons')
LOADING_STOP_PATH = os.path.join('.', 'images_lib', 'loading_gif', 'load_end.png')
LOADING_START_PATH = os.path.join('.', 'images_lib', 'loading_gif', 'load_{index}.png')
JSON_GAMEDATA_PATH = os.path.join('.', 'mcf_lib', 'GameData.json')
PAPICH_SONG_PATH = os.path.join('.', 'mcf_lib', 'song.mp3')
SPECTATOR_FILE_PATH = os.path.join('.', 'mcf_lib', 'spectate.bat')
SCREENSHOT_FILE_PATH = os.path.join('.', 'images_lib', 'screenshot_PIL.png')

"""
    Classes for finded game and switches for controling threads and activity 

"""
class MCFStorage:
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

class Switches:
    decorator = False
    request = False
    checkgame = False
    elorank = False
    delayed = False
    after_info = None
    after_delay = None
    calibration_index = 0

    def __str__(self) -> str:
        return f"""
        request: {self.request}
        checkgame: {self.checkgame}
        elorank: {self.elorank}
        delayed: {self.delayed}
        after_info: {self.after_info}
        after_delay: {self.after_delay}
        """