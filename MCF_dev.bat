@echo off
setlocal enabledelayedexpansion

rem Активируем виртуальное окружение
call .env\Scripts\activate.bat

rem Запускаем Python скрипт
py main.py RGAPI-5cfa8da7-3c6b-479c-ae1a-83d21019e6d7


