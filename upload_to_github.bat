@echo off
echo ====================================================================
echo   HAMILTON-JACOBI PDE RESEARCH SUITE - GITHUB UPLOADER
echo   Author: Samuel Hasiholan Omega Purba, S. Tr. T.
echo ====================================================================
echo.
set /p REPO_URL="Masukkan URL Repositori GitHub Anda (contoh: https://github.com/SamuelPurba/Hamilton-Jacobi-Solution.git): "

if "%REPO_URL%"=="" (
    echo [ERROR] URL tidak boleh kosong.
    pause
    exit /b
)

echo.
echo Adding remote origin...
git remote remove origin >nul 2>&1
git remote add origin %REPO_URL%

echo Setting main branch...
git branch -M main

echo.
echo Pushing to GitHub...
git push -u origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ====================================================================
    echo SUCCESS! Repositori berhasil diunggah ke GitHub dengan Top 1%% Quality!
    echo ====================================================================
) else (
    echo.
    echo [NOTICE] Jika diminta login, silakan ikuti instruksi otentikasi GitHub di browser/terminal.
)
echo.
pause
