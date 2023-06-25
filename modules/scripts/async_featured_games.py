import asyncio
import logging
from mcf_riot_api import RiotAPI
from aiohttp import ClientSession
from aiohttp.client_exceptions import (
    ClientProxyConnectionError,
    ClientConnectionError
)
from mcf_data import (
    ALL_CHAMPIONS_IDs,
    REGIONS_TUPLE,
    FEATURED_GAMES_URL,
    MCFStorage
)

def parse_games():
    """
        This function parsing games from Riot API Featured Games into
        GameData.json and returning count of missing regions
    
    """

    async def parsing(region):
        nonlocal missing_regions
        
        async with ClientSession() as session:
            async with session.get(url=FEATURED_GAMES_URL.format(region=region), 
                                   **RiotAPI.get_headers_timeeout()) as response:
                
                data = await response.json()
                gameList = data['gameList']

                
                try:
                    if len(gameList) < 1:
                        missing_regions += 1
                        return
                except KeyError:
                    missing_regions += 1
                    return

        
                routelist = []
                for s in range(0, len(gameList)):
                    
                    # Создаем список из id персонажей для дальнейшей конвертации в имени
                    id_names = [int(gameList[s]['participants'][k]['championId']) for k in range(5)]

                    # Создаем список конвертированных id в имена персонажей
                    champ_list = [ALL_CHAMPIONS_IDs.get(id_name) for id_name in id_names]
                    
                    champ_string = ' | '.join([str(item) for item in champ_list])
                    summoner = gameList[s]['participants'][0]['summonerName']
                    route = gameList[s]['platformId']

                    for r, g, _ in REGIONS_TUPLE:
                        if route.lower() == g: 
                            route = r.upper()
                            break
                            
                    routelist.append(f"{champ_string}-|-{summoner}:{route}")
                MCFStorage.write_data(
                    route=('MatchesARAM', region.upper(), ), 
                    value=routelist
                    )
                    
    async def main_aram():

        nonlocal missing_regions

        tasks = []
        for region in REGIONS_TUPLE:
            tasks.append(asyncio.create_task(parsing(region[1])))

        for task in tasks:
            try: 
                await asyncio.gather(task)
            except asyncio.exceptions.TimeoutError:
                missing_regions += 1
            except (ClientConnectionError, ClientProxyConnectionError):
                missing_regions = 20
                
    missing_regions = 0
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main_aram())
    
    return missing_regions
