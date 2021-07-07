@echo off

CALL %userprofile%\redenv\Scripts\activate.bat REM win
if [%1] == [] goto help

REM This allows us to expand variables at execution
setlocal ENABLEDELAYEDEXPANSION

goto %1

:reformat
%venv% isort .
%venv% black .
exit /B %ERRORLEVEL%

:isort
%venv% isort .
exit /B %ERRORLEVEL%

:black
%venv% black .
exit /B %ERRORLEVEL%

:stylediff
%venv% isort --atomic --check --diff --line-length 99 --use-parentheses .
%venv% black --check --diff -l 99 .
exit /B %ERRORLEVEL%

:help
echo Usage:
echo   make ^<command^>
echo.
echo Commands:
echo   reformat                   Reformat all .py files being tracked by git.
echo   isort                      Reformat all .py files only with isort.
echo   black                      Reformat all .py files only with black.
echo   stylediff                  Check .py files for style diffs.
