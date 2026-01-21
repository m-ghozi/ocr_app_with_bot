@echo off
echo ========================================
echo   Copy Tesseract Files to Project
echo ========================================
echo.

REM Check common Tesseract installation paths
set TESSERACT_PATH=

if exist "C:\Program Files\Tesseract-OCR\tesseract.exe" (
    set TESSERACT_PATH=C:\Program Files\Tesseract-OCR
    echo Found Tesseract at: C:\Program Files\Tesseract-OCR
) else if exist "C:\Tesseract-OCR\tesseract.exe" (
    set TESSERACT_PATH=C:\Tesseract-OCR
    echo Found Tesseract at: C:\Tesseract-OCR
) else if exist "C:\Tesseract-Temp\tesseract.exe" (
    set TESSERACT_PATH=C:\Tesseract-Temp
    echo Found Tesseract at: C:\Tesseract-Temp
) else (
    echo.
    echo Tesseract not found in common locations!
    echo.
    echo Please enter the path to your Tesseract installation:
    echo Example: C:\Program Files\Tesseract-OCR
    echo.
    set /p TESSERACT_PATH="Tesseract Path: "
)

echo.
echo Checking path: %TESSERACT_PATH%
echo.

if not exist "%TESSERACT_PATH%\tesseract.exe" (
    echo ERROR: tesseract.exe not found at: %TESSERACT_PATH%
    echo.
    pause
    exit /b 1
)

echo Creating tesseract folder...
if not exist "tesseract" mkdir tesseract

echo.
echo Copying files...
echo.

REM Copy tesseract.exe
echo [1/3] Copying tesseract.exe...
copy "%TESSERACT_PATH%\tesseract.exe" "tesseract\" >nul
if errorlevel 1 (
    echo ERROR: Failed to copy tesseract.exe
    pause
    exit /b 1
)
echo       ✓ tesseract.exe copied

REM Copy tessdata folder
echo [2/3] Copying tessdata folder...
xcopy "%TESSERACT_PATH%\tessdata" "tesseract\tessdata\" /E /I /Y /Q >nul
if errorlevel 1 (
    echo ERROR: Failed to copy tessdata folder
    pause
    exit /b 1
)
echo       ✓ tessdata folder copied

REM Copy all DLL files
echo [3/3] Copying DLL files...
copy "%TESSERACT_PATH%\*.dll" "tesseract\" >nul 2>&1
echo       ✓ DLL files copied

echo.
echo ========================================
echo SUCCESS! Tesseract files copied
echo ========================================
echo.
echo Folder structure:
echo tesseract\
echo ├── tesseract.exe
echo ├── tessdata\
echo │   └── eng.traineddata
echo └── *.dll files
echo.
echo Total size:
for /f "tokens=3" %%a in ('dir /s /-c "tesseract" ^| find "File(s)"') do set size=%%a
echo ~60-80 MB
echo.
echo Next step: Run build_portable.bat to create EXE
echo.
pause
