from mcf_data import (
    MCFStorage, 
    ten_roles_dict,
    eight_roles_dict
)
from mcf_build import MCFException

def get_aram_statistic(blue_entry: list, red_entry: list):

    def _change_total_matches_value(value):
        
        execute_value = [value, None]
        
        if value in range(7, 12):
            execute_value[1] = 'yellow'
        elif value < 7:
            execute_value[1] = 'red'       
        else:
            # execute_value[1] = '#65EC3B'
            execute_value[1] = '#8EF13C'
        
        return execute_value

    def _rate_chance_and_color(income_value, divider):
        '''
            divider: count of all games
            income_value: count of wins or totals
            out_value: float represent of winrate or total rate

        '''
        out_value = income_value / divider * 100

        match out_value, divider:
            case 100.0, div:
                return ['100%', '🟩']
            case 0, div:
                return ['0%', '🟥']
            case out, div if div in range(8, 12) and out >=80:
                if out >= 80: return [f"{'%.1f' % out}%", '🟩']
                if out <= 80: return [f"{'%.1f' % out}%", '🟥']
            case out, div if div <=7:
                return [f"{'%.1f' % out}%", '🟥']
            case out, div if out >= 66:
                return [f"{'%.1f' % out}%", '🟩']
            case out, div if out <= 66:
                return [f"{'%.1f' % out}%", '🟥']
            case _:
                return [f"{'%.1f' % out}%", 'white']

    def _find_games_from_stats(teams: dict[list], eight_roles=True):

        roles_strings = {
            'T1': ''.join(teams['T1']),
            'T2': ''.join(teams['T2'])
        }

        if eight_roles:
            with open('mcf_lib\Stats_Eight.txt', 'r') as stats:
                list_stats = stats.readlines()
        else:
            with open('.\mcf_lib\Stats_Ten.txt', 'r') as stats:
                list_stats = stats.readlines()

        target = None
        
        for match in list_stats:
            if match.startswith(f"{roles_strings['T1']}_{roles_strings['T2']}"):
                
                target = (match, 'blue')
                break
            elif match.startswith(f"{roles_strings['T2']}_{roles_strings['T1']}"):
                
                target = (match, 'red')
                break
        else:
            return None
        
        leader = target[1]
        results = target[0].split('|')
        w1_rate = results[1] if leader == 'blue' else results[2]
        w2_rate = results[1] if leader == 'red' else results[2]

        return {
                'w1': int(w1_rate),
                'w2': int(w2_rate),
                'tb': int(results[3]),
                'tl': int(results[4]),
                'all_m': int(results[5]),
                'all_ttl': int(results[6][:-1])
            }
    def _get_converted_roles(champ, eight_roles=True):
        if eight_roles:
            iter_dict = eight_roles_dict
        else:
            iter_dict = ten_roles_dict

        for i in iter_dict.items():
            if champ.lower().capitalize() in i[1]: 
                return i[0]
        
    teams = {
        'T1': blue_entry,
        'T2': red_entry,
    }

    if any([len(teams['T1']) < 5, len(teams['T2']) < 5]):
        raise MCFException(
            f"Not enough | T1: {5 - len(teams['T1'])} | T2: {5 - len(teams['T2'])}"
            )
    elif any([len(teams['T1']) > 5, len(teams['T2']) > 5]):
        raise MCFException(
            f"Extra | T1: {len(teams['T1']) - 5} | T2: {len(teams['T2']) - 5}"
            )
    else:
        MCFStorage.write_data(route=('Stats', ), value=teams)

    """
        Getting list of roles by converting character name into role index
    """
    teams_by_eight_roles = {
        'T1': sorted([_get_converted_roles(char, eight_roles=True) for char in teams['T1']]),
        'T2': sorted([_get_converted_roles(char, eight_roles=True) for char in teams['T2']]),
    }
    teams_by_ten_roles = {
        'T1': sorted([_get_converted_roles(char, eight_roles=False) for char in teams['T1']]),
        'T2': sorted([_get_converted_roles(char, eight_roles=False) for char in teams['T2']])
    }

    """
        Converting list of roles into string for comparing with items in .txt
    """
    
    eight_roles_rate = _find_games_from_stats(teams_by_eight_roles)
    ten_roles_rate = _find_games_from_stats(teams_by_ten_roles, eight_roles=False)
    
    match eight_roles_rate, ten_roles_rate:
        case None, None:
            final_result = {
                'w1': ['Нет данных', '❔'],
                'w2': ['Нет данных', '❔'],
                'tb': ['Нет данных', '❔'],
                'tl': ['Нет данных', '❔'],
                'all_m': '0',
                'all_ttl': '0'
            }
            return final_result
            # raise MCFException('No games finded')
        case None, rate:
            middle_rate = ten_roles_rate
        case rate, None:
            # print('this case')
            middle_rate = eight_roles_rate
        case _:
            middle_rate = {
                'w1': (eight_roles_rate['w1'] + ten_roles_rate['w1']),
                'w2': (eight_roles_rate['w2'] + ten_roles_rate['w2']),
                'tb': (eight_roles_rate['tb'] + ten_roles_rate['tb']),
                'tl': (eight_roles_rate['tl'] + ten_roles_rate['tl']),
                'all_m': eight_roles_rate['all_m'] + ten_roles_rate['all_m'],
                'all_ttl': eight_roles_rate['all_ttl'] + ten_roles_rate['all_ttl'],
            }

    final_result = {
        'w1': _rate_chance_and_color(int(middle_rate['w1']), int(middle_rate['all_m'])),
        'w2': _rate_chance_and_color(int(middle_rate['w2']), int(middle_rate['all_m'])),
        'tb': _rate_chance_and_color(int(middle_rate['tb']), int(middle_rate['all_ttl'])),
        'tl': _rate_chance_and_color(int(middle_rate['tl']), int(middle_rate['all_ttl'])),
        'all_m': _change_total_matches_value(middle_rate['all_m']),
        'all_ttl': _change_total_matches_value(middle_rate['all_ttl'])
    }

    # final_result = {
    #     'w1': _rate_chance_and_color(3, 3),
    #     'w2': _rate_chance_and_color(0, 3),
    #     'tb': _rate_chance_and_color(2, 3),
    #     'tl': _rate_chance_and_color(1, 3),
    #     'all_m': _change_total_matches_value(3),
    #     'all_ttl': _change_total_matches_value(3)
    # }
    
    return final_result    

    
