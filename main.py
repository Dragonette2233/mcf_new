from mcf_build import MCFWindow
from mcf_threads import MCFThread
import mcf_automized_bot
import mcf_testfield


if __name__ == '__main__':
    
    app = MCFWindow()
    app.bind("<Button-3>", app.rmc_callback)

    # app.context_menu.add_command(label="Открыть окно", command=lambda: print("TEST"))
    # app.context_menu.add_command(label="Действие 2", command=lambda: print("Действие 2"))
    # app.context_menu.add_separator()
    # app.context_menu.add_command(label="Выход", command=app.quit)
    
    app.context_menu.add_command(label='AUTOBOT', command=lambda: MCFThread(func=mcf_automized_bot.run_autobot).start())
    app.context_menu.add_command(label='AUTO_SCANNER', command=lambda: MCFThread(func=mcf_automized_bot.run_autoscanner).start())
    app.context_menu.add_command(label='PIL Calibration', command=app.change_calibration_index)
    app.context_menu.add_command(label='Close League', command=app.close_league_of_legends)
    app.context_menu.add_command(label='ARAM Timer', command=lambda: MCFThread(func=app.aram_porotimer).start())
    app.context_menu.add_command(label='Refresh', command=lambda: app.refresh())

####
    # import tkinter as tk

    # def rmc_callback(event):
    #     context_menu.post(event.x_root, event.y_root)

    # def open_window():
    #     new_window = tk.Toplevel(root)
    #     new_window.title("Новое окно")
    #     label = tk.Label(new_window, text="Пример нового окна")
    #     label.pack()

    # root = tk.Tk()
    # root.title("Пример контекстного меню")

    # # Создание контекстного меню
    # context_menu = tk.Menu(root, tearoff=0)
    # context_menu.add_command(label="Открыть окно", command=open_window)
    # context_menu.add_command(label="Действие 2", command=lambda: print("Действие 2"))
    # context_menu.add_separator()
    # context_menu.add_command(label="Выход", command=root.quit)

    # # Привязка контекстного меню к правой кнопке мыши
    # root.bind("<Button-3>", rmc_callback)
####
    
    
    
    app.mainloop()


