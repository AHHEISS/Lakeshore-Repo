@echo off

rem Set the path to your virtual environment's activate script
set "VENV_PATH=C:\Users\User Account\AppData\Local\Programs\Python\Lakeshore_Py\virt\Scripts\activate.bat"

rem Activate the virtual environment
call "%VENV_PATH%"

rem Change directory to where your executable is located
cd C:\Users\User Account\AppData\Local\Programs\Python\Lakeshore_Py

::  virt\Scripts\activate


rem Minimize the command window using a VBScript
echo Set objShell = CreateObject("WScript.Shell") > %temp%\minimize.vbs
echo objShell.SendKeys "%% n" >> %temp%\minimize.vbs
cscript //nologo %temp%\minimize.vbs
del %temp%\minimize.vbs

rem Run the standalone executable
start "" /B "dist\LakeshoreApp-U4.exe"

rem Optional: Add a pause to keep the command prompt window open (for debugging)
:: pause

rem The virtual environment will be automatically deactivated when the script exits
deactivate

rem Close the CMD window
exit
