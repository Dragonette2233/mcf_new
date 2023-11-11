from mcf_build import MCFWindow
import mcf_testfield

if __name__ == '__main__':
    
    app = MCFWindow()
    
    
    app.rmc_menu.add_command('PIL Calibration', command=app.change_calibration_index, button_forget=False)
    app.rmc_menu.add_command('Close League', command=app.close_league_of_legends)
    app.rmc_menu.add_command('Refresh', command=lambda: app.refresh())
    app.rmc_menu.add_command('ARAM Timer', command=app.aram_porotimer)
    
    app.mainloop()


