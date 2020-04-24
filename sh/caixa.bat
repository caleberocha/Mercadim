@echo off
pushd %~dp0..
if not exist venv python -m venv venv
call venv\scripts\activate.bat
pip install -r requirements.txt
python caixa.py
deactivate
popd