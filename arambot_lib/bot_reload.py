def close_mcf_and_chrome():
    import pygetwindow as gw

    # Указать заголовок окна, которое вы хотите закрыть
    wins_to_close = [
        'MCF_dev',
        'mcf_development',
        # 'Ставки на спорт',
        # 'Матчи онлайн'
    ]

    # Получение списка всех активных окон
    active_windows = gw.getAllTitles()

    # Вывод списка активных окон
    for window_title in active_windows:
        for w in wins_to_close:
            if str(window_title).startswith(w):
                gw.getWindowsWithTitle(window_title)[0].close()

def start_mcf():
    import os
    import subprocess

    # Получение значения переменной окружения MCF_ROOT
    mcf_root_path = os.environ.get('MCF_ROOT')

    if mcf_root_path:
        # Формирование пути к вашему .bat файлу, используя переменную окружения
        bat_file_path = os.path.join(mcf_root_path, 'MCF_dev.bat')

        # Запуск .bat файла с отдельной консолью
        try:
            subprocess.run(bat_file_path, shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
            print(f"Файл {bat_file_path} успешно запущен в отдельной консоли.")
        except FileNotFoundError:
            print(f"Файл {bat_file_path} не найден.")
        except Exception as e:
            print(f"Произошла ошибка при запуске {bat_file_path} в отдельной консоли: {e}")
    else:
        print("Переменная окружения MCF_ROOT не установлена.")




            

