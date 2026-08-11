@echo off
setlocal EnableExtensions

for %%I in ("%~dp0.") do set "REPO_DIR=%%~fI"
pushd "%REPO_DIR%" >nul 2>&1
if errorlevel 1 (
    echo [Ads] Cannot open the project folder.
    goto :failed_no_pop
)

where git >nul 2>&1
if errorlevel 1 (
    echo [Ads] Git is not installed or is not available in PATH.
    goto :failed
)

rem Allow this checkout when the launcher runs under a managed Windows account.
set "GIT_CONFIG_COUNT=1"
set "GIT_CONFIG_KEY_0=safe.directory"
set "GIT_CONFIG_VALUE_0=%REPO_DIR%"

git rev-parse --is-inside-work-tree >nul 2>&1
if errorlevel 1 (
    echo [Ads] This folder is not a Git repository.
    echo [Ads] Clone https://github.com/gaiautoupload/malpe.git first.
    goto :failed
)

for /f "delims=" %%B in ('git branch --show-current 2^>nul') do set "CURRENT_BRANCH=%%B"
if /I not "%CURRENT_BRANCH%"=="main" (
    echo [Ads] Please switch to the main branch before publishing images.
    echo [Ads] Current branch: %CURRENT_BRANCH%
    goto :failed
)

set "HAS_AD_CHANGES="
for /f "delims=" %%S in ('git status --short -- ad_image ad_image2 2^>nul') do set "HAS_AD_CHANGES=1"
if not defined HAS_AD_CHANGES (
    echo [Ads] No changes found in ad_image or ad_image2.
    goto :success
)

echo [Ads] The following advertisement image changes will be published:
git status --short -- ad_image ad_image2

if /I "%~1"=="/dry-run" (
    echo [Ads] Dry run completed. No files were committed or pushed.
    goto :success
)

choice /C YN /N /M "[Ads] Publish these changes to origin/main? [Y/N]: "
if errorlevel 2 (
    echo [Ads] Cancelled.
    goto :success
)

git config user.name >nul 2>&1
if errorlevel 1 (
    echo [Ads] Git user.name is not configured.
    echo [Ads] Run: git config --global user.name "Your Name"
    goto :failed
)

git config user.email >nul 2>&1
if errorlevel 1 (
    echo [Ads] Git user.email is not configured.
    echo [Ads] Run: git config --global user.email "you@example.com"
    goto :failed
)

echo [Ads] Checking the latest origin/main...
git fetch origin main
if errorlevel 1 (
    echo [Ads] Could not fetch origin/main. Nothing was committed.
    goto :failed
)

git add -A -- ad_image ad_image2
git diff --cached --quiet -- ad_image ad_image2
if not errorlevel 1 (
    echo [Ads] No publishable image changes remain after staging.
    goto :success
)

for /f "delims=" %%T in ('powershell -NoProfile -Command "Get-Date -Format yyyy-MM-dd_HH-mm-ss"') do set "PUBLISH_TIME=%%T"
if not defined PUBLISH_TIME set "PUBLISH_TIME=manual"

git commit -m "Update advertisement images %PUBLISH_TIME%"
if errorlevel 1 (
    echo [Ads] Commit failed. The image files remain staged.
    goto :failed
)

git rebase origin/main
if errorlevel 1 (
    echo [Ads] Remote changes conflict with this image update.
    echo [Ads] The rebase will be aborted; the local commit is preserved.
    git rebase --abort >nul 2>&1
    goto :failed
)

git push origin main
if errorlevel 1 (
    echo [Ads] Push failed. The image commit is preserved locally.
    echo [Ads] Resolve the reported problem, then run this file again.
    goto :failed
)

echo [Ads] Advertisement images were published successfully.
echo [Ads] Other computers will download them on their next launch.

:success
popd >nul 2>&1
if /I not "%~1"=="/dry-run" pause
exit /b 0

:failed
popd >nul 2>&1
:failed_no_pop
pause
exit /b 1
