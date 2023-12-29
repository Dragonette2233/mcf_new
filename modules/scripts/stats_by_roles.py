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
            case out, div if div in range(9, 15):
                if out >= 80: return [f"{'%.1f' % out}%", '🟩']
                if out < 80: return [f"{'%.1f' % out}%", '🟥']
            case out, div if div < 9:
                return [f"{'%.1f' % out}%", '🟥']
            case out, div if out >= 65:
                return [f"{'%.1f' % out}%", '🟩']
            case out, div if out < 65:
                return [f"{'%.1f' % out}%", '🟥']
            case _:
                return [f"{'%.1f' % out}%", 'white']

    def _find_games_from_stats(teams: dict[list]):

        roles_strings = {
            'T1': ''.join(teams['T1']),
            'T2': ''.join(teams['T2'])
        }

        
        with open('.\mcf_lib\stats_migrated.txt', 'r') as stats:
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
    teams_by_ten_roles = {
        'T1': sorted([_get_converted_roles(char, eight_roles=False) for char in teams['T1']]),
        'T2': sorted([_get_converted_roles(char, eight_roles=False) for char in teams['T2']])
    }

    """
        Converting list of roles into string for comparing with items in .txt
    """
    
    ten_roles_rate = _find_games_from_stats(teams_by_ten_roles)
    
    if ten_roles_rate is None:
        final_result = {
                'w1': ['0%', '🟥'],
                'w2': ['0%', '🟥'],
                'tb': ['0%', '🟥'],
                'tl': ['0%', '🟥'],
                'all_m': '0',
                'all_ttl': '0'
            }
        return final_result

    else:
        final_result = {
        'w1': _rate_chance_and_color(int(ten_roles_rate['w1']), int(ten_roles_rate['all_m'])),
        'w2': _rate_chance_and_color(int(ten_roles_rate['w2']), int(ten_roles_rate['all_m'])),
        'tb': _rate_chance_and_color(int(ten_roles_rate['tb']), int(ten_roles_rate['all_ttl'])),
        'tl': _rate_chance_and_color(int(ten_roles_rate['tl']), int(ten_roles_rate['all_ttl'])),
        'all_m': _change_total_matches_value(ten_roles_rate['all_m']),
        'all_ttl': _change_total_matches_value(ten_roles_rate['all_ttl'])
    }
        
    return final_result

    
