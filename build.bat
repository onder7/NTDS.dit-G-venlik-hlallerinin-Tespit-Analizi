@echo off
echo NTDS.dit Analyzer - Build Process Starting

REM Create dist and build folders if they don't exist
if not exist "dist" mkdir dist
if not exist "build" mkdir build

REM Clean previous builds
rmdir /s /q dist
rmdir /s /q build

REM Create exe with PyInstaller
pyinstaller --noconfirm ^
    --clean ^
    --name "NTDS_Analyzer" ^
    --icon="icon.ico" ^
    --noconsole ^
    --add-data "icon.ico;." ^
    --hidden-import "tkinter" ^
    --hidden-import "subprocess" ^
    --hidden-import "datetime" ^
    --hidden-import "threading" ^
    --hidden-import "re" ^
    --hidden-import "os" ^
    --hidden-import "webbrowser" ^
    ntds_analyzer.py

echo Build process completed
pause
