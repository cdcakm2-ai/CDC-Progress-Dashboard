@echo off
set "PATH=%~dp0tools\mingit\cmd;%PATH%"
echo ======================================================================
echo  Uploading Akmeemana Praja Dashboard to GitHub...
echo  Target: https://github.com/cdcakm2-ai/CDC-Progress-Dashboard
echo ======================================================================
echo.
git push -u origin main
echo.
pause
