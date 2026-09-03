@echo off
setlocal
pushd "%~dp0"

echo [Launcher] Closing previous main.py process if it is running...
powershell -NoProfile -ExecutionPolicy Bypass -Command "$target = [IO.Path]::GetFullPath((Join-Path (Get-Location) 'main.py')); Get-CimInstance Win32_Process -Filter \"Name = 'python.exe' OR Name = 'pythonw.exe'\" | Where-Object { $_.CommandLine -and $_.CommandLine -match [regex]::Escape($target) } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }"

call "%~dp0git_update.bat"
python main.py
popd
pause
