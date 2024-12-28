@echo off

REM Проверка наличия Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python не установлен. Установка Python...
    REM Скачивание Python
    powershell -Command "Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.11.5/python-3.11.5-amd64.exe -OutFile python_installer.exe"
    REM Установка Python
    python_installer.exe /quiet InstallAllUsers=1 PrependPath=1
    del python_installer.exe
    echo Python установлен.
) else (
    echo Python уже установлен.
)

REM Обновление pip
echo Обновление pip...
python -m ensurepip --upgrade
python -m pip install --upgrade pip

REM Установка необходимых библиотек
echo Установка библиотек...
python -m pip install opencv-python pillow

REM Запуск программы
echo Запуск программы animation.py...
python animation.py

pause
