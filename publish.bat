@echo off
setlocal

pushd "%~dp0"
set "GIT_CONFIG_COUNT=1"
set "GIT_CONFIG_KEY_0=safe.directory"
set "GIT_CONFIG_VALUE_0=%CD%"
set "GIT_TERMINAL_PROMPT=0"

where git >nul 2>&1
if errorlevel 1 (
    echo [Git] Git is not installed.
    popd
    pause
    exit /b 1
)

git rev-parse --is-inside-work-tree >nul 2>&1
if errorlevel 1 (
    echo [Git] This folder is not a Git repository.
    popd
    pause
    exit /b 1
)

for /f "delims=" %%T in ('powershell -NoProfile -Command "Get-Date -Format 'yyyy-MM-dd HH:mm:ss'"') do set "COMMIT_TIME=%%T"

git add -A
git diff --cached --quiet
if not errorlevel 1 (
    echo [Git] No changes to publish.
    popd
    pause
    exit /b 0
)

git commit -m "Update game plugin %COMMIT_TIME%"
if errorlevel 1 (
    echo [Git] Commit failed.
    popd
    pause
    exit /b 1
)

git push origin main
if errorlevel 1 (
    echo [Git] Push failed. The commit remains local.
    popd
    pause
    exit /b 1
)

echo [Git] Published successfully: %COMMIT_TIME%
popd
pause
