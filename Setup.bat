@echo off

REM Prompt user to check for Flask installation
set /p checkFlask="Do you want to check if Flask is installed? (y/n): "
if /i "%checkFlask%"=="y" (
    python -c "import flask" 2>NUL
    if %ERRORLEVEL% NEQ 0 (
        echo Flask not found.
        REM Prompt user to install Flask
        set /p installFlask="Flask is missing. Do you want to install Flask? (y/n): "
        if /i "%installFlask%"=="y" (
            pip install flask
        ) else (
            echo Skipping Flask installation.
        )
    ) else (
        echo Flask is already installed.
    )
) else (
    echo Skipping Flask check.
)

REM Prompt user to run the CreateTable.py script
set /p runScript="Do you want to run database setup? (y/n): "
if /i "%runScript%"=="y" (
    python ./backend/Scripts/CreateTable.py
) else (
    echo Skipping CreateTable.py execution.
)

pause