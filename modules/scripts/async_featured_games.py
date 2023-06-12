import gc
import asyncio
import logging
from mcf_riot_api import RiotAPI
from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientProxyConnectionError
from mcf_data import (
    ALL_CHAMPIONS_IDs,
    REGIONS_TUPLE,
    MCFStorage
)

def parse_games():

    async def parsing(region):
        nonlocal missing_regions
        
        async with ClientSession() as session:
            url = f"https://{region}.api.riotgames.com/lol/spectator/v4/featured-games"
            
            async with session.get(url=url, **RiotAPI.get_headers()) as response_:
                
                response = await response_.json()
                
                try:
                    if len(response['gameList']) < 1:
                        missing_regions += 1
                        return
                except KeyError:
                    missing_regions += 1
                    return

        
                routelist = []
                for s in range(0, len(response['gameList'])):
                    
                    # Создаем список из id персонажей для дальнейшей конвертации в имени
                    id_names = [int(response['gameList'][s]['participants'][k]['championId']) for k in range(5)]

                    # Создаем список конвертированных id в имена персонажей
                    champ_list = [ALL_CHAMPIONS_IDs.get(id_name) for id_name in id_names]
                    
                    champ_string = ' | '.join([str(item) for item in champ_list])
                    summoner = response['gameList'][s]['participants'][0]['summonerName']
                    route = response['gameList'][s]['platformId']

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
            except ClientProxyConnectionError:
                missing_regions = 20
                
    missing_regions = 0
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main_aram())
    
    return missing_regions
