@echo off
setlocal enabledelayedexpansion
title La Mia Gioia - AI Studio Photo Generator

echo ================================================================
echo       LA MIA GIOIA - AI STUDIO PHOTO GENERATOR (PHOTOROOM)
echo ================================================================
echo.

:: 1. Check Python installation (check 'py' launcher or 'python')
set "PY_CMD="
where py >nul 2>nul
if %errorlevel% equ 0 (
    set "PY_CMD=py"
) else (
    where python >nul 2>nul
    if %errorlevel% equ 0 (
        set "PY_CMD=python"
    )
)

if "%PY_CMD%"=="" (
    if exist "%LOCALAPPDATA%\Programs\Python\Python314\python.exe" (
        set "PY_CMD=%LOCALAPPDATA%\Programs\Python\Python314\python.exe"
    ) else if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
        set "PY_CMD=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
    ) else if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" (
        set "PY_CMD=%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
    )
)

if "%PY_CMD%"=="" (
    echo [ERROR] Python is not found on your system PATH!
    echo Please install Python 3.8 or higher from https://www.python.org/
    echo During installation, be sure to check "Add Python to PATH".
    echo.
    pause
    exit /b 1
)

:: 2. Install required packages
echo [1/3] Checking dependencies...
%PY_CMD% -m pip install -q -r requirements.txt
if %errorlevel% neq 0 (
    echo [WARNING] Retrying dependency installation...
    %PY_CMD% -m pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install packages from requirements.txt.
        echo.
        pause
        exit /b 1
    )
)
echo [1/3] Dependencies verified.
echo.

:: 3. Verify PHOTOROOM_API_KEY
echo [2/3] Checking Photoroom API key...
if "%PHOTOROOM_API_KEY%"=="" (
    echo [!] Environment variable PHOTOROOM_API_KEY is not set.
    set /p USER_API_KEY="Please enter your Photoroom API Key: "
    if "!USER_API_KEY!"=="" (
        echo [ERROR] No API key provided! Photoroom requires an active API key.
        echo Get your API key at: https://photoroom.com/api
        echo.
        pause
        exit /b 1
    )
    set "PHOTOROOM_API_KEY=!USER_API_KEY!"
)
echo [2/3] API key configured.
echo.

:: 4. Execute python generator
echo [3/3] Running studio photo generator...
echo ----------------------------------------------------------------
%PY_CMD% generate_studio_photos.py
set SCRIPT_EXIT_CODE=%errorlevel%
echo ----------------------------------------------------------------
echo.

if %SCRIPT_EXIT_CODE% equ 0 (
    echo [SUCCESS] Studio photo generation finished successfully!
    echo Processed photos are located in the "processed_bags" folder.
) else (
    echo [!] Process completed with errors (Exit code: %SCRIPT_EXIT_CODE%).
)

echo.
pause
