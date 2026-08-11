@echo off
setlocal EnableExtensions

for %%I in ("%~dp0.") do set "PROJECT_DIR=%%~fI"
pushd "%PROJECT_DIR%" >nul 2>&1
if errorlevel 1 (
    echo [Environment] Cannot open the project folder.
    goto :failed_no_pop
)

set "PYTHON_EXE="
set "PYTHON_ARGS="

where py >nul 2>&1
if not errorlevel 1 (
    set "PYTHON_EXE=py"
    set "PYTHON_ARGS=-3"
    goto :python_found
)

where python >nul 2>&1
if not errorlevel 1 (
    set "PYTHON_EXE=python"
    goto :python_found
)

echo [Environment] Python 3 was not found.
echo [Environment] Install Python from https://www.python.org/downloads/windows/
echo [Environment] Enable "Add Python to PATH" during installation.
goto :failed

:python_found
if not exist "%PROJECT_DIR%\requirements.txt" (
    echo [Environment] requirements.txt was not found.
    goto :failed
)

echo [Environment] Using Python:
%PYTHON_EXE% %PYTHON_ARGS% --version
if errorlevel 1 (
    echo [Environment] The detected Python command is not working.
    goto :failed
)

echo [Environment] Preparing pip...
%PYTHON_EXE% %PYTHON_ARGS% -m ensurepip --upgrade
if errorlevel 1 (
    echo [Environment] Could not prepare pip.
    goto :failed
)

%PYTHON_EXE% %PYTHON_ARGS% -m pip install --upgrade pip
if errorlevel 1 (
    echo [Environment] Could not update pip.
    goto :failed
)

echo [Environment] Installing Python packages from requirements.txt...
%PYTHON_EXE% %PYTHON_ARGS% -m pip install -r "%PROJECT_DIR%\requirements.txt"
if errorlevel 1 (
    echo [Environment] Package installation failed.
    goto :failed
)

echo [Environment] Checking installed package compatibility...
%PYTHON_EXE% %PYTHON_ARGS% -m pip check
if errorlevel 1 (
    echo [Environment] Installed packages have dependency conflicts.
    goto :failed
)

if not exist "C:\Program Files\Tesseract-OCR\tesseract.exe" (
    echo.
    echo [Environment] Python packages are installed, but Tesseract OCR is missing.
    echo [Environment] Install Tesseract OCR at:
    echo [Environment] C:\Program Files\Tesseract-OCR\tesseract.exe
    goto :failed
)

echo.
echo [Environment] Installation completed successfully.
echo [Environment] You can now run start.bat or start_main_no_round0.bat.
popd >nul 2>&1
pause
exit /b 0

:failed
popd >nul 2>&1
:failed_no_pop
echo.
echo [Environment] Installation did not complete. Review the message above.
pause
exit /b 1
