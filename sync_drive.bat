@echo off
set "PATH=%~dp0tools\mingit\cmd;%PATH%"
title Akmeemana Praja Dashboard - Google Drive Sync
echo ======================================================================
echo   Akmeemana CDC Progress Dashboard - Google Drive Sync
echo ======================================================================
echo.
echo [1/3] Checking Google Drive for new files / modifications...
python scripts/auto_drive_sync_once.py
if errorlevel 1 goto error

echo.
echo [2/3] Checking git changes...
git status -s > "%TEMP%\git_status.txt"
for %%R in ("%TEMP%\git_status.txt") do if %%~zR==0 (
    echo No new data changes to upload. Dashboard is already up-to-date!
    goto done
)

echo.
echo [3/3] Uploading updated data to Live Website (GitHub Pages)...
git add -A
git commit -m "data: live sync with Google Drive update"
git push origin main
if errorlevel 1 goto error

:done
echo.
echo ======================================================================
echo   SUCCESS! The live website is updated!
echo   Live URL: https://cdcakm2-ai.github.io/CDC-Progress-Dashboard/
echo ======================================================================
echo.
pause
exit /b 0

:error
echo.
echo ======================================================================
echo   [NOTICE] Sync could not complete. Check your internet connection.
echo ======================================================================
echo.
pause
