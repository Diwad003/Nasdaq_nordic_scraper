@echo off
:: Get the current date in yyyy-mm-dd format
for /f "tokens=1-4 delims=.-/ " %%a in ('date /t') do (
    set year=%%a
    set month=%%b
    set day=%%c
)

:: Format the date as yyyy-mm-dd
set currentDate=%year%-%month%-%day%
set dir=.\data\%currentDate%\


:: Run the Python script with the formatted date
python3 .\CompanyScraper.py https://www.nasdaqomxnordic.com/shares/listed-companies/stockholm %dir%
pause