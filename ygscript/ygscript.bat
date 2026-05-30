@echo off
REM YGScript - Command line wrapper

setlocal enabledelayedexpansion

REM Get the directory of this script
set SCRIPT_DIR=%~dp0

REM Run Python with the main script
python "%SCRIPT_DIR%src\ygscript.py" %*

endlocal
