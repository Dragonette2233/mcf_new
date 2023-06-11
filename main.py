from mcf_build import MCFWindow
from mcf_data import Switches
from mcf_data import currentGameData

if __name__ == '__main__':
    
    app = MCFWindow()
    # app.info_view.display_info('Some info')
    app.rmc_menu.add_command('debug lastgame', 
                             command=lambda: app.obj_gamechecker._debug_lastgame())
    app.rmc_menu.add_command('cnv check', 
                             command=lambda: print(app.canvas.find_all()))
    app.rmc_menu.add_command('test circle', 
                             command=lambda: app.canvas.start_circle())
    app.rmc_menu.add_command('switch aram/rift logo', 
                             command=lambda: app.canvas.test_switch_request())
    app.rmc_menu.add_command('current game data', 
                             command=lambda: print(currentGameData))
    app.rmc_menu.add_command('Refresh checker', 
                             command=lambda: app.refresh())
    
    app.mainloop()


