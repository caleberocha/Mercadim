@echo off
pushd %~dp0..
call venv\scripts\activate.bat
python api.py
deactivate
popd