from mcf_build import MCFWindow
from mcf_data import currentGameData
from mcf_threads import MCFThread
from mcf_data import Switches
import threading

def debugMode(event):

    selftest = test_app.obj_gamechecker.entry.get()
    match selftest:
        case 'my':
            test_app.obj_gamechecker.entry.delete(0, 'end')
            test_app.obj_gamechecker.entry.insert(0, 'myloveisafteryou:EUW')
            MCFThread(func=test_app.obj_gamechecker.search_for_game).start()
        case 'last':
            test_app.info_view.display_info(text='DBG: Last game', ground='white', delay=1.5)
            # global sw_switches, GAMEDATA
            currentGameData.area = 'europe'
            currentGameData.region = 'euw1'
            currentGameData.game_id = '5942324637'
            currentGameData.match_id = 'EUW1_5942324637'
            Switches.request = True
            test_app.after(1500, lambda: MCFThread(func=test_app.obj_gamechecker.awaiting_game_end).start())
        case 'cnv':
            test_app.info_view.display_info(
                text=f'DBG: canvas: {test_app.canvas.find_all()}',
                delay=2.5,
                ground='white'
            )
        case 'ts':
            subprocess.Popen(['notepad.exe', 'TASKS.txt'])
        case 'spc':
            runSpectator()
        case 'replay_a':
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
        case 'frame':
            ...
            # canvas.diplay_info()
            # root.placeframe()
            # tk.Label().pack()
        case _:
            test_app.info_view.display_info(text='DBG: unknown command', ground='white', delay=1.5)
            # showMainInfo(text='DEBUG CMD: my, last, cnv, ts, rft, asd', seconds=2.5, ground='white')

test_app = MCFWindow()

test_app.obj_gamechecker.entry.bind('<Control-w>', debugMode)
