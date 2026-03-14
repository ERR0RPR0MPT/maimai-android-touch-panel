@echo off
:loop
python .\main.py
if %errorlevel% == 42 goto loop
