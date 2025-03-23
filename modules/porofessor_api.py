



class PoroAPI:

    __headers_timeout = {
        'headers': { 
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36" },
        'timeout': 3
    }
    # __link_rnk_solo = 'https://porofessor.gg/current-games/{champion}/queue-420'
    # __link_rnk_flex = 'https://porofessor.gg/current-games/{champion}/queue-440'
    __link_aram = 'https://porofessor.gg/current-games/{champion}/queue-450'

    @RiotAPI.connection_handler
    @staticmethod
    def get_poro_games(red_champion):
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

        try:
            url = PoroAPI.__link_aram.format(champion=converted_champion)
        except:
            raise MCFException('This gamemod is unaccesible')
                
        result = requests.get(url, **PoroAPI.__headers_timeout)
        soup: bs = bs(result.text, "html.parser").find_all('div', class_='cardTeam')

        if result.status_code != 200:
            raise MCFException(f'Error. Status: {result.status_code}')
        
        games = {
            'teams': [team.find_all('img') for i, team in enumerate(soup) if i % 2 == 0],
            'champions': [],
            # 'nicknames': [team.find('div', class_='name').text.strip() for i, team in enumerate(soup) if i % 2 == 0],
            'regions': [team.find('a', class_='liveGameLink').get('href') for i, team in enumerate(soup) if i % 2 == 0],
            'elorank': [team.find('div', class_='subname').text.strip() for i, team in enumerate(soup) if i % 2 == 0]
        }


        nicknames = [[ch.text.strip() for ch in team.find_all('div', class_='name')] for i, team in enumerate(soup) if i % 2 == 0]

        # print(nicknames)
        


        for game in games['teams']:
            
            for i, champ in enumerate(game):
                if len(champ.get('class')) == 0:
                   del game[i]

            ids = []

            for info_stroke in game:
                champ_id_wieght = info_stroke.get('class')
                
                if len(champ_id_wieght) > 0:
                    ids.append(int(champ_id_wieght[0].split('-')[1]))
                    
            converted_ids = [ALL_CHAMPIONS_IDs.get(i) for i in ids]
            games['champions'].append(converted_ids)

        featured_games = []
       

        for c, n, r in zip(games['champions'], nicknames, games['regions']): # games['elorank']):
            
            champs = ' | '.join(c)
            names_region = '_|_'.join([f"{name}:{r.split('/')[2].upper()}" for name in n])
            whole_string = f"{champs}-|-{names_region}"
            featured_games.append(whole_string)
        
        MCFStorage.write_data(route=('MatchesRift', ), value=featured_games)