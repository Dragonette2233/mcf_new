from mcf_build import MCFWindow
from mcf_threads import MCFThread
import mcf_automized_bot


if __name__ == '__main__':
    
    app = MCFWindow()
    
    app.rmc_menu.add_command('AUTOBOT', command=lambda: MCFThread(func=mcf_automized_bot.run_autobot).start())
    app.rmc_menu.add_command('PIL Calibration', command=app.change_calibration_index, button_forget=False)
    app.rmc_menu.add_command('Close League', command=app.close_league_of_legends)
    app.rmc_menu.add_command('ARAM Timer', command=lambda: MCFThread(func=app.aram_porotimer).start())
    app.rmc_menu.add_command('Refresh', command=lambda: app.refresh())
    
    
    
    app.mainloop()


