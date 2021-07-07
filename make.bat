@echo off

if [%1] == [] goto help

REM This allows us to expand variables at execution
setlocal ENABLEDELAYEDEXPANSION

REM Edit after venv= for your own venv
set venv=%userprofile%\redenv\Scripts\activate.bat
goto %1

:reformat
%venv% isort .
%venv% black .
exit /B %ERRORLEVEL%

:help
echo Usage:
echo   make ^<command^>
echo.
echo Commands:
echo   reformat                   Reformat all .py files being tracked by git.
