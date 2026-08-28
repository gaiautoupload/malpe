@echo off
setlocal

for %%I in ("%~dp0.") do set "REPO_DIR=%%~fI"
pushd "%REPO_DIR%" >nul 2>&1
if errorlevel 1 (
    echo [Git] Cannot open project folder. Skipping update check.
    exit /b 0
)

where git >nul 2>&1
if errorlevel 1 (
    echo [Git] Git is not installed. Skipping update check.
    goto :finish
)

rem Allow this checkout when the launcher runs under a managed Windows account.
set "GIT_CONFIG_COUNT=1"
set "GIT_CONFIG_KEY_0=safe.directory"
set "GIT_CONFIG_VALUE_0=%REPO_DIR%"

git rev-parse --is-inside-work-tree >nul 2>&1
if errorlevel 1 (
    echo [Git] This folder is not a Git repository. Skipping update check.
    goto :finish
)

for /f "delims=" %%B in ('git branch --show-current 2^>nul') do set "CURRENT_BRANCH=%%B"
if not defined CURRENT_BRANCH (
    echo [Git] Detached HEAD detected. Skipping automatic update.
    goto :check_local_ads
)

rem All launcher computers must follow the shared main branch.
set CURRENT_BRANCH=main

echo [Git] Checking origin/%CURRENT_BRANCH% for updates...
set "GIT_TERMINAL_PROMPT=0"
git fetch --quiet origin "%CURRENT_BRANCH%"
if errorlevel 1 (
    echo [Git] Update check failed. Starting with the local version.
    goto :check_local_ads
)

echo [Git] Overwriting local tracked files with origin/main...
git reset --hard origin/main
if errorlevel 1 (
    echo [Git] Automatic overwrite failed. Starting with the local version.
    goto :check_local_ads
)

for /f "delims=" %%C in ('git rev-list --count HEAD..origin/%CURRENT_BRANCH% 2^>nul') do set "UPDATE_COUNT=%%C"
if not defined UPDATE_COUNT (
    echo [Git] Could not compare local and remote versions.
    goto :check_local_ads
)

if "%UPDATE_COUNT%"=="0" (
    echo [Git] Already up to date.
    goto :check_local_ads
)

echo [Git] Found %UPDATE_COUNT% new commit(s):
git diff --name-status HEAD "origin/%CURRENT_BRANCH%"

git diff --quiet HEAD "origin/%CURRENT_BRANCH%" -- ad_image ad_image2
if errorlevel 1 (
    echo [Git] Advertisement images have updates in ad_image or ad_image2.
) else (
    echo [Git] No advertisement image changes in this update.
)

git merge --ff-only "origin/%CURRENT_BRANCH%"
if errorlevel 1 (
    echo [Git] Automatic update failed, possibly because of local changes.
    echo [Git] Starting with the current local version.
) else (
    echo [Git] Update completed.
)

:check_local_ads
for /f "delims=" %%S in ('git status --short -- ad_image ad_image2 2^>nul') do set "LOCAL_AD_CHANGES=1"
if defined LOCAL_AD_CHANGES (
    echo [Git] Warning: ad_image or ad_image2 has uncommitted local changes.
) else (
    echo [Git] Advertisement image folders are clean.
)

:finish
popd >nul 2>&1
exit /b 0
