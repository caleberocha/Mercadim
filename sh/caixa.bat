@echo off
pushd %~dp0..
call venv\scripts\activate.bat
python caixa.py
deactivate
popd