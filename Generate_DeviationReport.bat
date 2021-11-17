@echo off
setlocal enableextensions enabledelayedexpansion
rem +---------------------------------------------------------+
rem | Author : M.W.Richardson                                 |
rem | Date   : 20/06/2016                                     |
rem |                                                         |
rem | Generates a deviation report                            |
rem | Searches over all c, c++, h files and lists all lines   |
rem | that contain LDRA_INSPECTED                             |
rem |                                                         |
rem | Copyright : (c) 2016 Liverpool Data Research Associates |
rem +---------------------------------------------------------+

set prj=MinGW_Cashregister
set Report=DeviationReport.xml
set NTP=%PROGRAMFILES(X86)%\Notepad++
set TempFile=temp.txt

echo ^<?xml version="1.0" encoding="UTF-8"?^> > %Report%
echo ^<Project="%prj%"^> >> %Report%

rem iterate over all c and c++ files
rem ================================
for /R %%f in (*.c,*.cpp,*.h) do (
  set "fname=%%~nxf"
  rem ignore any instrumented file
  if "!fname!"=="!fname:inszt=!" (
	  echo   ^<file name="!fname!" path="%%f"^> >> %Report%
    FINDSTR /n "LDRA_INSPECTED" %%f > %TempFile%
    for /f "tokens=*" %%i in (!TempFile!) do (
		  echo     ^<Justification^> >> %Report%
		rem  echo       ^<Text=%%i^> >> %Report%
      for /f "tokens=1,2,3 delims=:" %%a in ("%%i") do (
			  set rule=%%b
				set rule=!rule:/*LDRA_INSPECTED=!
				set rule=!rule://LDRA_INSPECTED=!
				call :Trim rule !rule!
				set desc=%%c
				call :Trim desc !desc!
        if "!desc:~-1!"=="/" set desc=!desc:~0,-2!
				call :Trim desc !desc!
			  echo       ^<Comment line="%%a" rule="!rule!" description="!desc!"^/^> >> %Report%
			)
		  echo     ^<^/Justification^> >> %Report%
		)
    echo   ^<^/file^> >> %Report%
  )
)
echo ^</Project^> >> %Report%

if exist %TempFile% del /F %TempFile%

if exist %Report% goto P1
pause
exit

:P1
if exist "%NTP%\notepad++.exe" goto P2
%TBED%\TBbrowse %Report%
exit

:P2
"%NTP%\notepad++" %Report%
exit

:Trim
SetLocal EnableDelayedExpansion
set Params=%*
for /f "tokens=1*" %%a in ("!Params!") do EndLocal & set %1=%%b
exit /b
