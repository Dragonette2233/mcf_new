@echo off
setlocal enabledelayedexpansion

rem Активируем виртуальное окружение
call .env\Scripts\activate.bat

rem Запускаем Python скрипт
py main.py [riot-api-key]


