from mcf_build import MCFWindow
from mcf_threads import MCFThread
import mcf_automized_bot
import mcf_testfield


if __name__ == '__main__':
    
    app = MCFWindow()
    app.bind("<Button-3>", app.rmc_callback)

    app.context_menu.add_command(label='AUTOBOT', command=lambda: MCFThread(func=mcf_automized_bot.run_autobot).start())
    app.context_menu.add_command(label='AUTO_SCANNER', command=lambda: MCFThread(func=mcf_automized_bot.run_autoscanner).start())
    app.context_menu.add_command(label='PIL Calibration', command=app.change_calibration_index)
    app.context_menu.add_command(label='Close League', command=app.close_league_of_legends)
    app.context_menu.add_command(label='ARAM Timer', command=lambda: MCFThread(func=app.aram_porotimer).start())
    app.context_menu.add_command(label='Refresh', command=lambda: app.refresh())

    
    app.mainloop()


