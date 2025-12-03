@echo off
REM Quick script to push to GitHub after you create the repository

echo ========================================
echo  Push to GitHub
echo ========================================
echo.

REM Check if git is initialized
if not exist ".git" (
    echo ERROR: Git not initialized!
    pause
    exit /b 1
)

echo.
echo STEP 1: Create your GitHub repository
echo ----------------------------------------
echo 1. Go to: https://github.com/new
echo 2. Repository name: pdf-receipt-api
echo 3. Visibility: Public
echo 4. DON'T check any boxes
echo 5. Click "Create repository"
echo.

set /p USERNAME="Enter your GitHub username: "

echo.
echo STEP 2: Pushing to GitHub...
echo ----------------------------------------

REM Add remote
git remote remove origin 2>nul
git remote add origin https://github.com/%USERNAME%/pdf-receipt-api.git

REM Push
echo Pushing code to GitHub...
git branch -M main
git push -u origin main

echo.
echo ========================================
echo  ✅ Code pushed to GitHub!
echo ========================================
echo.
echo Your repository: https://github.com/%USERNAME%/pdf-receipt-api
echo.
echo NEXT: Deploy on Render.com
echo 1. Go to: https://render.com
echo 2. Sign in with GitHub
echo 3. New + → Web Service
echo 4. Connect: pdf-receipt-api
echo 5. Click "Create Web Service"
echo.

pause
