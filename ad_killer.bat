@echo off
call "%~dp0git_update.bat"
pushd "%~dp0"
python ad_killer.py
popd
pause
