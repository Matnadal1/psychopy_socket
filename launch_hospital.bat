@echo off
echo Starting RSVP Experiment - Hospital Environment
echo ============================================
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.
echo Launching experiment...
python launch_rsvp.py hospital
echo.
pause
