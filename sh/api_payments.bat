@echo off
pushd %~dp0..
call venv\scripts\activate.bat
python api_payments.py
deactivate
popd