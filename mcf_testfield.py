from mcf_build import MCFWindow
from mcf_data import currentGameData
from mcf_threads import MCFThread
from mcf_data import Switches
from modules.scripts import async_poro_games
import threading
from mcf_riot_api import TGApi
# import time

def get_val():
    # import pyautogui
    import time
    while True:
        diff_check = app_test_context.get_diff_for_stream()
        if diff_check == 0:
            break
        app_test_context.info_view.exception('No stream_yet')
        time.sleep(2)
    time.sleep(1)
    app_test_context.mcf_click(x=271, y=1054, double=True)
    time.sleep(0.25)
    app_test_context.mcf_click(x=328, y=972)
    while True:
        app_test_context.mcf_click(x=658, y=828, double=True)  
        app_test_context.generate_score()
        time.sleep(3)

def debugMode(event):

    selftest = app_test_context.obj_gamechecker.entry.get()
    match selftest:
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
