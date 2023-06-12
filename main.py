from mcf_build import MCFWindow
from mcf_data import Switches
from mcf_data import currentGameData
import mcf_testfield


def check_gamedata_test():

    # print(currentGameData.response['gameId'] if currentGameData.response.get('gameId') else 'Nothing here')
    print(currentGameData)
    # print(currentGameData.game_id)
    # print(currentGameData.match_id)

if __name__ == '__main__':
    
    app = MCFWindow()
    # app.info_view.display_info('Some info')
    app.rmc_menu.add_command('debug lastgame', 
                             command=lambda: app.obj_gamechecker._debug_lastgame())
    app.rmc_menu.add_command('cnv check', 
                             command=lambda: print(app.canvas.find_all()))
    app.rmc_menu.add_command('test currentGameData', 
                             command=check_gamedata_test)
    app.rmc_menu.add_command('switch aram/rift logo', 
                             command=lambda: app.canvas.test_switch_request())
    app.rmc_menu.add_command('current game data', 
                             command=lambda: print(currentGameData))
    app.rmc_menu.add_command('Refresh checker', 
                             command=lambda: app.refresh())
    
    app.mainloop()


