@echo off
REM SNB Installation Script for Windows
REM This script sets up SNB to be accessible from anywhere in the command line

echo ========================================
echo SNB (Save 'N' Backup) - Installation
echo ========================================
echo.

REM Get the current directory (where snb.py is located)
set "SNB_DIR=%~dp0"
set "SNB_DIR=%SNB_DIR:~0,-1%"

echo SNB Directory: %SNB_DIR%
echo.

REM Create a batch file wrapper in the same directory
echo Creating snb.bat wrapper...
(
echo @echo off
echo python "%SNB_DIR%\snb.py" %%*
) > "%SNB_DIR%\snb.bat"

if exist "%SNB_DIR%\snb.bat" (
    echo [OK] snb.bat created successfully
) else (
    echo [ERROR] Failed to create snb.bat
    pause
    exit /b 1
)

echo.
echo ========================================
echo Adding SNB to PATH
echo ========================================
echo.

REM Check if the directory is already in PATH
echo %PATH% | findstr /C:"%SNB_DIR%" >nul
if %errorlevel% equ 0 (
    echo [INFO] SNB directory is already in PATH
    goto :done
)

REM Add to user PATH permanently
echo Adding %SNB_DIR% to user PATH...
for /f "skip=2 tokens=3*" %%a in ('reg query HKCU\Environment /v PATH 2^>nul') do set "CURRENT_PATH=%%b"

if not defined CURRENT_PATH (
    set "NEW_PATH=%SNB_DIR%"
) else (
    set "NEW_PATH=%CURRENT_PATH%;%SNB_DIR%"
)

REM Update registry
reg add HKCU\Environment /v PATH /t REG_EXPAND_SZ /d "%NEW_PATH%" /f >nul

if %errorlevel% equ 0 (
    echo [OK] PATH updated successfully
    echo.
    echo [IMPORTANT] Please restart your terminal/command prompt
    echo             for the changes to take effect.
) else (
    echo [ERROR] Failed to update PATH
    echo.
    echo Please add the following directory to your PATH manually:
    echo %SNB_DIR%
)

:done
echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Usage:
echo   snb nmap -sV example.com
echo   snb gobuster dir -u http://example.com -w wordlist.txt
echo   echo "test" ^| snb
echo.
echo Output will be saved to: snb_outputs\[tool-name]\snb_DD.MM.YYYY.txt
echo.
echo [!] Remember to restart your terminal if PATH was updated!
echo.
pause
