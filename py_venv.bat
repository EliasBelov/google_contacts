@echo off
SETLOCAL

REM Проверка наличия папки venv
IF NOT EXIST "%~dp0venv" (
    echo Creating virtual environment...
    virtualenv venv
    CALL "%~dp0venv\Scripts\activate.bat"
    pip install patool	
    python.exe -m pip install --upgrade pip
    mkdir src
    mkdir lib    
    
)


REM Создание main.py
IF NOT EXIST "%~dp0main.py" (
    "" > "%~dp0main.py"
)


REM Копирование файла archive.py в текущую директорию
IF NOT EXIST "%~dp0archive.py" (
    echo Copying archive.py to current directory...
    chcp 65001
    xcopy /Y "%USERPROFILE%\Desktop\archive.py" "%~dp0"
    chcp 437
    python.exe archive.py -c "first archive"
)


REM ВЫПОЛНЯЕТСЯ В ПОСЛЕДНЮЮ ОЧЕРЕДЬ Запуск ConEmu с активированным виртуальным окружением
start "" "C:\Program Files\ConEmu\ConEmu64.exe" /cmd cmd /k "cd /d %~dp0venv\Scripts && call activate.bat && cd.. && cd.."


ENDLOCAL
@echo on