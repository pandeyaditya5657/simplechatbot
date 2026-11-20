@echo off
cd /d "%~dp0"
set PYCMD=
where py >nul 2>nul && set PYCMD=py -3
if "%PYCMD%"=="" where python >nul 2>nul && set PYCMD=python
if "%PYCMD%"=="" (
  echo Python was not found. Install it from https://www.python.org/downloads/
  echo and tick "Add Python to PATH" during setup.
  pause
  exit /b 1
)
%PYCMD% launcher.py
pause
