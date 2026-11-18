@echo off
setlocal enabledelayedexpansion
title Akmeemana Praja Dashboard - GitHub Uploader
cls
echo ======================================================================
echo    AKMEEMANA PRAJA DASHBOARD - GITHUB UPLOAD HELPER
echo ======================================================================
echo.

set "PATH=%~dp0tools\mingit\cmd;%PATH%"

echo 1. Checking git status...
git status -s
echo.

set /p REPO_URL="GitHub Repository URL eka methanata paste karanna (Enter URL): "
if "%REPO_URL%"=="" (
    echo.
    echo [ERROR] Repository URL ekak laba nodunneya.
    echo Karunakara https://github.com/username/repo-name.git lesa paste karanna.
    pause
    exit /b 1
)

echo.
echo 2. Setting remote origin to: %REPO_URL%
git remote remove origin 2>nul
git remote add origin %REPO_URL%
git branch -M main

echo.
echo 3. Uploading (Pushing) to GitHub main branch...
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ======================================================================
    echo  [SUCCESS] Code eka GitHub ekata kamyab lesa upload una!
    echo ======================================================================
    echo.
    echo Dan GitHub Pages hadaganna:
    echo 1. GitHub repo eke Settings ^> Pages yanna.
    echo 2. Source: "Deploy from a branch", Branch: "main", Folder: "/ (root)" thorala Save karanna.
    echo 3. Vinadi 1-2 kin oyage Live URL eka labei!
) else (
    echo.
    echo [NOTE] Sign in wenna ahuwoth GitHub browser sign in eka complete karanna.
)

echo.
pause
