@echo off
echo.
echo 🚀 Auto GitHub Setup Script for Python Project
echo ---------------------------------------------

:: Set Git user details
git config --global user.name "Hitesh Kumar Jangir"
git config --global user.email "hiteshjangir6517@gmail.com"

:: Set project directory
set "PROJECT_DIR=C:\Users\HR\Downloads\Compressed\py_to_exe"
echo 📁 Project folder: %PROJECT_DIR%

cd /d %PROJECT_DIR%

:: Check if Python file exists
if not exist "app.py" (
    echo ❌ Python file app.py not found in the folder!
    pause
    exit /b
)

:: Check if HTML file exists
if not exist "templates\index.html" (
    echo ❌ HTML file index.html not found in the templates folder!
    pause
    exit /b
)

:: Initialize Git if not initialized
git rev-parse --is-inside-work-tree >nul 2>&1
if %errorlevel% neq 0 (
    echo 🔧 Initializing Git repository...
    git init
)

:: Add files to git staging area
echo 🔨 Adding files to Git...
git add .

:: Commit with a message
echo 💬 Committing changes...
git commit -m "Added app.py and index.html for Flask app"

:: Set remote repository URL
set REMOTE_URL=https://github.com/hiteshjangir8057/py_to_exe-converter.git

:: Add remote URL
git remote add origin %REMOTE_URL%

:: Push to GitHub (main first, fallback to master)
echo 🚀 Pushing to GitHub...
git push -u origin main || git push -u origin master

echo ✅ Done! Your project is now pushed to GitHub.
pause
