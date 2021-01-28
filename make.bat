@echo off

if [%1] == [] goto help

REM This allows us to expand variables at execution
setlocal ENABLEDELAYEDEXPANSION

goto %1

:reformat
isort --atomic --line-length 99 --use-parentheses .
black -l 99 .
exit /B %ERRORLEVEL%

:help
echo Usage:
echo   make ^<command^>
echo.
echo Commands:
echo   reformat                   Reformat all .py files being tracked by git.
