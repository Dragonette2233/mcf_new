from mcf_build import MCFWindow
from mcf_threads import MCFThread
import mcf_automized_bot


if __name__ == '__main__':
    
    app = MCFWindow()
    app.bind("<Button-3>", app.rmc_callback)
    MCFThread(func=app.init_processing).start()

    app.context_menu.add_command(label='AUTOBOT', command=lambda: MCFThread(func=mcf_automized_bot.run_autobot).start())
    app.context_menu.add_command(label='Close League', command=app.close_league_of_legends)
    app.context_menu.add_command(label='TG_Notification', command=app.toogle_telegram_bot)
    app.context_menu.add_command(label='Refresh', command=lambda: app.refresh())

    app.mainloop()


