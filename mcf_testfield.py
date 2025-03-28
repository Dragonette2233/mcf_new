from mcf_build import MCFWindow
from mcf_data import (
    currentGameData,
    MCFStorage
)
from mcf_threads import MCFThread
from mcf_data import Switches, Validator
from modules.scripts import (
    ssim_recognition
)
import threading
# from PIL import ImageGrab
from mcf_riot_api import PoroAPI
from mcf_riot_api import TGApi
from PIL import ImageGrab
# import time
from mcf_data import MCF_BOT_PATH
import sys
import os


# sys.path.append(os.path.join(MCF_BOT_PATH, 'mcf'))



SW = True

def test_score_tab():

    from modules.scripts import mcf_autogui

    mcf_autogui.open_score_tab()

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
    global SW
    selftest = app_test_context.obj_gamechecker.entry.get()
    match selftest:
        case 'green':
            global ImageGrab
            # from PIL import ImageGrab
            
            rect = ImageGrab.grab().crop((76, 865, 174, 867))
            result = tesg.check_green_fill(rect)
            app_test_context.info_view.success(f"Green: {result}")
            
        case 'shot':
            from PIL import ImageGrab
            ImageGrab.grab().save('./shot.png')
        case 'tws_stop':
            SW = False
        case 'tws':
            from modules.scripts import mcf_autogui
            from PIL import ImageGrab
            import time

            def _thread_tws():
                blue_shot = None
                red_shot = None
                blue_backup = 0
                red_backup = 0
                counter = 0
                mcf_autogui.click(1770, 976)
                while True:
                    score = ssim_recognition.ScoreRecognition.screen_score_recognition()
                    if score['red_towers'] == 0:
                        mcf_autogui.click(1752, 970)
                        time.sleep(0.07)
                        mcf_autogui.doubleClick(936, 620)
                        time.sleep(0.07)
                        blue_shot = ImageGrab.grab()
                        blue_t1_health = ssim_recognition.ScoreRecognition.towers_healh_recognition(image=blue_shot)
                        if not blue_t1_health:
                            blue_t1_health = blue_backup
                        else:
                            blue_backup = blue_t1_health
                    else:
                        blue_t1_health = 0

                    if score['blue_towers'] == 0:
                        mcf_autogui.click(1811, 919)
                        time.sleep(0.07)
                        mcf_autogui.doubleClick(951, 490)
                        time.sleep(0.07)
                        red_shot = ImageGrab.grab()
                        red_t1_health = ssim_recognition.ScoreRecognition.towers_healh_recognition(image=red_shot)
                        if not red_t1_health:
                            red_t1_health = red_backup
                        else:
                            red_backup = red_t1_health
                    else:
                        red_t1_health = 0
                    counter += 1
                     # f"{'%.1f' % out}%"
                    app_test_context.info_view.notification(f"BL T1: {blue_t1_health}% | RD T1: {red_t1_health}%")
                    
                    # if counter == 10:
                    break

            MCFThread(func=_thread_tws).start()

        case 'asparse':
            from modules.scripts import mcf_utils
            mcf_utils.async_poro_parsing('Garen')
            print('done')
        case 'scoredata_shot':
            from PIL import ImageGrab
            screen = ImageGrab.grab()
            image = screen.crop((681, 7, 1261, 99))
            image.save('score.png')
        case 'scr':
            app_test_context.after(3000, test_score_tab)
        case 'gettime':
            data = ssim_recognition.ScoreRecognition.screen_score_recognition()
                
            app_test_context.info_view.success(
                    f"G:{data['blue_gold']}_{data['red_gold']}|TW: {data['blue_towers']}_{data['red_towers']}"
            )
            # import time
            # def _gettime():
            #     while True:
                    
            #         time.sleep(2)
            # MCFThread(func=_gettime).start()
            
            # MCFStorage.save_score(score=data)
            # print(data)
        case sc_test if sc_test.startswith('sct'):
            # app_test_context.info_view.notification('SCT starts with')
            # app_test_context.generate_score()

            # example: sct__bl_tw:0
            dict_data = {}
            data = sc_test.split('__')[1]

            key, value = data.split(':')
            dict_data[key] = value

            # app_test_context.info_view.notification(f'SCT starts with {data}')
            # print(dict_data)
            ssim_recognition.ScoreRecognition.collecting_ssim_data(**dict_data)
            app_test_context.info_view._display_info(f'SCT {data} done', delay=0.6, ground='green')
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
