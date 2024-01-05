from mcf_build import MCFWindow
from mcf_data import currentGameData
from mcf_threads import MCFThread
from mcf_data import Switches, Validator
from modules.scripts import async_poro_games
import threading
from mcf_riot_api import PoroAPI
from mcf_riot_api import TGApi

from PIL import Image, ImageGrab
import os
import numpy as np
from skimage.metrics import structural_similarity as ssim
# import time
GTIME_DATA_PATH = os.path.join('.', 'ssim_score_data', 'gametime')
BLUE_SCORE_PATH = os.path.join('.', 'ssim_score_data', 'team_blue', 'score_{pos}')
RED_SCORE_PATH =  os.path.join('.', 'ssim_score_data', 'team_red', 'score_{pos}')
BLUE_TOWER_PATH = os.path.join('.', 'ssim_score_data', 'team_blue', 'towers')
RED_TOWER_PATH = os.path.join('.', 'ssim_score_data', 'team_red', 'towers')


def get_compare(cut_image, type, position, team=None):

    match type, position, team:
        case 'gtime', 0, None:
            main_images = [Image.open(os.path.join(GTIME_DATA_PATH, f'{position}', f'{i}.png')) for i in range(4)]
        case 'gtime', 1 | 3, None:
            main_images = [Image.open(os.path.join(GTIME_DATA_PATH, f'{position}', f'{i}.png')) for i in range(10)]
        case 'gtime', 2, None:
            main_images = [Image.open(os.path.join(GTIME_DATA_PATH, f'{position}', f'{i}.png')) for i in range(6)]
        case 'score', pos, 'blue':
            main_images = [Image.open(os.path.join(BLUE_SCORE_PATH.format(pos=pos), f'{i}.png')) for i in range(10)]
        case 'score', pos, 'red':
            main_images = [Image.open(os.path.join(RED_SCORE_PATH.format(pos=pos), f'{i}.png')) for i in range(10)]
        case 'towers', pos, 'blue':
            main_images = [Image.open(os.path.join(BLUE_TOWER_PATH, f'{i}.png')) for i in range(5)]
        case 'towers', pos, 'red':
            main_images = [Image.open(os.path.join(RED_TOWER_PATH, f'{i}.png')) for i in range(5)]
        case _:
            print(type, team, position)
            raise ValueError('Undefined value in get_compare()') 
            # return
    
    main_images_arr = [np.array(img) for img in main_images]

    for idx, compare_img in enumerate(main_images_arr):
        similarity_index = ssim(compare_img, cut_image)

        # Если найдено более высокое сходство, сохраняем его и путь к изображению
        if similarity_index > 0.93:
            return idx
    else:
        return ''    

def screen_score_recognition():

    screen = ImageGrab.grab()
    image = screen.crop((681, 7, 1261, 99))
    
    final_time = [
        get_compare(np.array(image.crop((264, 72, 271, 85)).convert('L')), 'gtime', 0),
        get_compare(np.array(image.crop((273, 72, 280, 85)).convert('L')), 'gtime', 1),
        get_compare(np.array(image.crop((287, 72, 294, 85)).convert('L')), 'gtime', 2),
        get_compare(np.array(image.crop((296, 72, 304, 85)).convert('L')), 'gtime', 3)
    ]

    blue_score = [
        get_compare(np.array(image.crop((225, 18, 242, 41)).convert('L')), 'score', 0, 'blue'),
        get_compare(np.array(image.crop((243, 18, 260, 41)).convert('L')), 'score', 1, 'blue')
    ]

    red_score = [
        get_compare(np.array(image.crop((309, 18, 328, 41)).convert('L')), 'score', 0, 'red'),
        get_compare(np.array(image.crop((329, 18, 347, 41)).convert('L')), 'score', 1, 'red')
    ]

    blue_towers = get_compare(np.array(image.crop((35, 14, 47, 29)).convert('L')), 'towers', 0, 'blue')
    red_towers = get_compare(np.array(image.crop((559, 14, 571, 29)).convert('L')), 'towers', 0, 'red')

    str_final_time = f'{final_time[0]}{final_time[1]}:{final_time[2]}{final_time[3]}' # XX:XX

    if blue_score[0] == 0:
        blue_score.remove(0)

    str_blue_score = ''.join([str(i) for i in blue_score])
    str_red_score = ''.join([str(i) for i in red_score])

    app_test_context.info_view.success(f'Time: {str_final_time}  | Blue: {str_blue_score} ({blue_towers}) Red: {str_red_score} ({red_towers})')
    
def collecting_ssim_data(**kwargs):

    screen = ImageGrab.grab()
    image = screen.crop((681, 7, 1261, 99))

    if 'bl_tw' in kwargs:
        image.crop((35, 14, 47, 29)).convert('L').save(os.path.join('.', 'ssim_score_data', 'team_blue', 'towers', f'{kwargs["bl_tw"]}.png')) # work
    if 'rd_tw' in kwargs:
        image.crop((559, 14, 571, 29)).convert('L').save(os.path.join('.', 'ssim_score_data', 'team_red', 'towers', f'{kwargs["rd_tw"]}.png')) # work

    if 'bl_sc_0' in kwargs:
        image.crop((225, 18, 242, 41)).convert('L').save(os.path.join('.', 'ssim_score_data', 'team_blue', 'score_0', f'{kwargs["bl_sc_0"]}.png')) # work
    if 'bl_sc_1' in kwargs:
        image.crop((243, 18, 260, 41)).convert('L').save(os.path.join('.', 'ssim_score_data', 'team_blue', 'score_1', f'{kwargs["bl_sc_1"]}.png')) # work

    if 'rd_sc_0' in kwargs:
        image.crop((309, 18, 328, 41)).convert('L').save(os.path.join('.', 'ssim_score_data', 'team_red', 'score_0', f'{kwargs["rd_sc_0"]}.png')) # work
    if 'rd_sc_1' in kwargs:
        image.crop((329, 18, 347, 41)).convert('L').save(os.path.join('.', 'ssim_score_data', 'team_red', 'score_1', f'{kwargs["rd_sc_1"]}.png')) # work

    if 'g_0' in kwargs:
        image.crop((264, 72, 271, 85)).convert('L').save(os.path.join('.', 'ssim_score_data', 'gametime', '0', f'{kwargs["g_0"]}.png')) # # 6x13
    if 'g_1' in kwargs:
        image.crop((273, 72, 280, 85)).convert('L').save(os.path.join('.', 'ssim_score_data', 'gametime', '1', f'{kwargs["g_1"]}.png'))
    if 'g_2' in kwargs:
        image.crop((287, 72, 294, 85)).convert('L').save(os.path.join('.', 'ssim_score_data', 'gametime', '2', f'{kwargs["g_2"]}.png'))
    if 'g_3' in kwargs:
        image.crop((296, 72, 304, 85)).convert('L').save(os.path.join('.', 'ssim_score_data', 'gametime', '3', f'{kwargs["g_3"]}.png')) 



def stats_register_test(values_list):

    for val, key in enumerate(Validator.stats_register):

        Validator.stats_register[key] = values_list[val]

def simm_test():
    app_test_context.info_view.notification('Processing images...')
    from test_recog_ssim import RecognizedCharacters
    team_blue = RecognizedCharacters(team_color='blue')
    team_red = RecognizedCharacters(team_color='red')
    app_test_context.info_view.success('Processing done.')

    charlist_blue = team_blue.run()
    charlist_red = team_red.run()

    app_test_context.refresh()
    app_test_context.obj_aram.blue_entry.insert(0, ' '.join(charlist_blue))
    app_test_context.obj_aram.red_entry.insert(0, ' '.join(charlist_red))
    app_test_context.info_view.success(f'Blue: {len(charlist_blue)} | Red {len(charlist_red)}')

def debugMode(event):
    # print('work')
    selftest = app_test_context.obj_gamechecker.entry.get()
    match selftest:
        case 'gettime':
            MCFThread(func=screen_score_recognition).start()
        case sc_test if sc_test.startswith('sct'):
            # app_test_context.info_view.notification('SCT starts with')
            # app_test_context.generate_score()
            dict_data = {}
            data = sc_test.split('__')[1]

            key, value = data.split(':')
            dict_data[key] = value

            # app_test_context.info_view.notification(f'SCT starts with {data}')
            # print(dict_data)
            collecting_ssim_data(**dict_data)
            app_test_context.info_view._display_info(f'SCT {data} done', delay=0.3, ground='green')
            # data_values = {
            #         'g_0': 0,
            #         'g_1': 0,
            #         'g_2': 0,
            #         'g_3': 0,
            #         'bl_sc_0': 0,
            #         'bl_sc_1': 0,
            #         'bl_tw': 0,
            #         'rd_sc_0': 0,
            #         'rd_sc_1': 0,
            #         'rd_tw': 0
            #     }

        case 's_show':
            print(Validator.stats_register)
        case val if val.startswith('s_reg'):
            reg_switches = val.split(':')[1]
            stats_register_test([int(i) for i in reg_switches])
            print(Validator.stats_register)
        case 'flparse':
            app_test_context.info_view.notification('Parsing from RiotAPI and Poro...')
            async_poro_games.parse_games(champion_name='Vayne') # Parse full PoroARAM by region
            PoroAPI.get_poro_games(red_champion='Vayne') # Parse only main page PoroARAM
            app_test_context.info_view.success('Done')
        case 'ssim':
            MCFThread(func=simm_test).start()
        case 'gen_compare':
            from PIL import ImageGrab
            import os

            screen = ImageGrab.grab()
            crops = screen.crop((1675, 839, 1764, 887))
            crops.save(os.path.join('.', 'images_lib', 'build_compare.png'))

        case 'click':
            app_test_context.mcf_click(x=271, y=1054)
        case 'scgen':
            app_test_context.generate_score()
        case 'difo':
            MCFThread(func=get_val).start()
        case selftest if selftest.startswith('tg:'):
            message = selftest.split(':')[1]
            TGApi.send_simple_message(message=message)

        case 'score':
            score = app_test_context.get_gamescore()
            print(type(score))
        case 'tall_test':
            async_poro_games.parse_games('lebl')
        case 'thr_active':
            app_test_context.info_view._display_info(text=f"Active threads: {threading.activeCount()}", ground='white', delay=1.5)
            # print(threading.activeCount())
        case 'my':
            app_test_context.obj_gamechecker.entry.delete(0, 'end')
            app_test_context.obj_gamechecker.entry.insert(0, 'myloveisafteryou:EUW')
            MCFThread(func=app_test_context.obj_gamechecker.search_for_game).start()
        case 'last':
            app_test_context.info_view._display_info(text='DBG: Last game', ground='white', delay=1.5)
            # global sw_switches, GAMEDATA
            currentGameData.area = 'europe'
            currentGameData.region = 'euw1'
            currentGameData.game_id = '5942324637'
            currentGameData.match_id = 'EUW1_5942324637'
            Switches.request = True
            app_test_context.after(1500, lambda: MCFThread(func=app_test_context.obj_gamechecker.awaiting_game_end).start())
        case 'cnv':
            app_test_context.info_view._display_info(
                text=f'DBG: canvas: {app_test_context.canvas.find_all()}',
                delay=2.5,
                ground='white'
            )
        case 'ts':
            subprocess.Popen(['notepad.exe', 'TASKS.txt'])
        case 'viewable':
            print(app_test_context.obj_featured.button_aram_get.winfo_viewable())
            app_test_context.obj_featured.button_aram_get.place_forget()
            print(app_test_context.obj_featured.button_aram_get.winfo_viewable())
        case 'len_entry':
            entry = app_test_context.obj_aram.blue_entry.get().strip().split(' ')
            print(len(entry))
            print(entry)
            ...
            # subprocess.Popen(["start", "cmd", "/k", r"py .\replays_poro.py ARAM"], shell = True)
        case 'replay_r':
            ...
            # subprocess.Popen(["start", "cmd", "/k", r"py .\replays_poro.py RIFT"], shell = True)
        case 'thrs':
            for i in threading.enumerate():
                print(i.name)
        case 'sw_status':
            print(Switches())
        case 'current_game':
            print(currentGameData)
        case 'attr':
            value = 'obj_aram.blue_entry'
            obj, entry = value.split('.')
            # value =  
            # attrs = [app_test_context.__getattribute__(attr)[k].config(state='disabled') for attr, k in zip(objects_, keys)]
            print(app_test_context.__getattribute__(obj.entry).__getattribute__(entry))
        case 'frame':
            ...
            # canvas.diplay_info()
            # root.placeframe()
            # tk.Label().pack()
        case _:
            app_test_context.info_view._display_info(text='DBG: unknown command', ground='white', delay=1.5)
            # showMainInfo(text='DEBUG CMD: my, last, cnv, ts, rft, asd', seconds=2.5, ground='white')

app_test_context = MCFWindow()

# app_test_context.rmc_menu.add_command('DBG: current game data', 
#                             command=lambda: print(currentGameData))

app_test_context.obj_gamechecker.entry.bind('<Control-w>', debugMode)
