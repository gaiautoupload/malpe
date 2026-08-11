@echo off
call "%~dp0git_update.bat"
pushd "%~dp0"
python main_no_round0.py
popd
pause
