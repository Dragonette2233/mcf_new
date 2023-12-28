from string import punctuation, digits, whitespace
from mcf_build import MCFException
from mcf_data import (
    MCFStorage, 
    ALL_CHAMPIONS_IDs,
)

"""
    This module interact with games in GameData.json

"""

def get_games_by_character(character: str, state: str = ''):

    for symbol in punctuation + digits + whitespace:
        if symbol in character:
            raise MCFException('Exclude wrong symbol and try again')
    
    if state == 'aram_api':
        matches_by_regions = MCFStorage.get_selective_data(route=('MatchesAPI', ))
        all_matches = [item for sublist in matches_by_regions.values() for item in sublist]
    elif state == 'aram_poro':
        matches_by_regions = MCFStorage.get_selective_data(route=('MatchesARAM', ))
        all_matches = [item for sublist in matches_by_regions.values() for item in sublist]
    else:
        all_matches = MCFStorage.get_selective_data(route=('MatchesRift', ))
        
    finded_games = set()

    for p in ALL_CHAMPIONS_IDs.values():
        if p.casefold().startswith(character.casefold()):
            character = p
            break
    else:
        raise MCFException(f'Who is {character}')
    

    #if character 

    for match in all_matches:
        # print(match)
        if character in match:
            print(match)
            print(character)
            finded_games.add(match)

    # for match in all_matches:
    #     if character.casefold() in [m.casefold() for m in match]:
    #         finded_games.add(match)
            

    
    # if len(finded_games) == 0:
    #     raise MCFException(f'No matches for {character}')
    
    return list(finded_games)