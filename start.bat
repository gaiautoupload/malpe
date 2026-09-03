@echo off
setlocal
pushd "%~dp0"

echo [Launcher] Closing previous main.py and main_no_round0.py processes if running...
powershell -NoProfile -ExecutionPolicy Bypass -Command "$targets = @('main.py','main_no_round0.py') | ForEach-Object { [regex]::Escape([IO.Path]::GetFullPath((Join-Path (Get-Location) $_))) }; Get-CimInstance Win32_Process -Filter \"Name = 'python.exe' OR Name = 'pythonw.exe'\" | ForEach-Object { $process = $_; if ($process.CommandLine -and ($targets | Where-Object { $process.CommandLine -match $_ })) { Stop-Process -Id $process.ProcessId -Force -ErrorAction SilentlyContinue } }"

call "%~dp0git_update.bat"
python main.py
popd
pause
