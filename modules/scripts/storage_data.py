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
        print(all_matches)
    else:
        all_matches = MCFStorage.get_selective_data(route=('MatchesRift', ))
        
    finded_games = set()

    for p in ALL_CHAMPIONS_IDs.values():
        if p.casefold().startswith(character.casefold()):
            character = p
            break
    else:
        raise MCFException(f'Who is {character}')
        
    for match in all_matches:
        if character in match:
            finded_games.add(match)
            

    # if len(finded_games) > 5:
    #    raise MCFException(f'{len(finded_games)} games with {character}')
    
    if len(finded_games) == 0:
        raise MCFException(f'No matches for {character}')
    
    return list(finded_games)

    
    for enum, button in enumerate(canvas.obj_featured['txt_btns']):

        splited: list = button['text'].strip().split(' | ')
        splited.sort()
        assembled = '_'.join(s.strip() for s in splited)
        
        if stringCompare.casefold() == assembled.casefold():
            button['fg'] = '#25D500'