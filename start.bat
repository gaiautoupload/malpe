@echo off
call "%~dp0git_update.bat"
pushd "%~dp0"
python main.py
popd
pause
