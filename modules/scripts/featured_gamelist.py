from string import punctuation, digits, whitespace
from mcf_riot_api import MCFException
from mcf_data import (
    MCFStorage, 
    ALL_CHAMPIONS_IDs,
)
from pprint import pprint


def get_games_by_character(character: str, aram=True):

    def _check_for_wrong_symbols(entry):

        for symbol in punctuation + digits + whitespace:
            if symbol in entry:
                raise MCFException('Exclude wrong symbol and try again')
                
    # def _create_button(button: tk.Button, champion, name):

    #     button.configure(
    #         command=lambda: _destroy_button(name),
    #         text=f' {champion} '
    #     )
    
    # def _destroy_button(name_region):
    #     # global cnv_images, sw_switches
    #     name_region = name_region.split(':')
    #     putToEntry(f"{':'.join(name_region[0:2])}", canvas.obj_match_c['entry'])

    #     # if len(name_region) == 3:
    #     #     cnv_images['eloimage'] = create_ranked_image(name_region[2])
    #     #     Switches.elorank = True
    #     # else:
    #     #     Switches.elorank = False

    #     for button in canvas.featured_frames:
    #         button.place_forget()


    if aram:
        _check_for_wrong_symbols(character)
        matches_by_regions = MCFStorage.get_selective_data(route=('MatchesARAM', ))
        all_matches = (item for sublist in matches_by_regions.values() for item in sublist)
        
    else:
        
        _check_for_wrong_symbols(character)
           
        with open('.\mcf_lib\GamesPoro.json', 'r', encoding='utf-8') as jsondata:
            matches = json.load(jsondata)
        
        if event == 'aram':
            matches = matches['aram']
        else:
            matches = matches['ranked-solo']
            # matches = getJsonData(key='MatchesRift', execute=True)

    '''Featured games dict'''
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
            

    if len(finded_games) > 5:
        raise MCFException(f'{len(finded_games)} games with {character}')
    
    if len(finded_games) == 0:
        raise MCFException(f'No matches for {character}')
    
    return list(finded_games)

    if canvas.featured_frames[0].winfo_viewable() == 1:

        for i in canvas.featured_frames: i.place_forget()

    for i, y in zip(range(names_finded), [152, 177, 202, 227, 252]):
        kwargs = {
            'button': canvas.obj_featured['txt_btns'][i],
            'champion': finded_games['champs'][i],
            'name': finded_games['names'][i]
        }
        _create_button(**kwargs)

        match len(canvas.find_overlapping(4,200,170,160)):
            case 4:
                canvas.featured_frames[i].place(x=190, y=y)
            case _:
                canvas.featured_frames[i].place(x=70, y=y)
            
    for enum, frame in enumerate(canvas.featured_frames):
        frame['highlightbackground'] = '#339999'
        canvas.obj_featured['txt_btns'][enum]['fg'] = 'white'

    for enum, button in enumerate(canvas.obj_featured['txt_btns']):

        splited: list = button['text'].strip().split(' | ')
        splited.sort()
        assembled = '_'.join(s.strip() for s in splited)
        
        if stringCompare.casefold() == assembled.casefold():
            button['fg'] = '#25D500'