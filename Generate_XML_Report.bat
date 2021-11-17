
@echo off
rem +---------------------------------------------------------+
rem | Author : M.W.Richardson                                 |
rem | Date   : 20/06/2016                                     |
rem |                                                         |
rem | Uses the GLHAPI to get all results and print them in    |
rem | XML format                                              |
rem |                                                         |
rem | Copyright : (c) 2016 Liverpool Data Research Associates |
rem +---------------------------------------------------------+

set TBED="C:\_LDRA_Toolsuite\988_RC1"
set WORKAREA="C:\_LDRA_Workarea\988_RC1"
set NTP=%PROGRAMFILES(X86)%\Notepad++
set SET_NAME=Cashregister

set GLH_FILE=%WORKAREA%\%SET_NAME%_tbwrkfls\%SET_NAME%.glh
set XML_FILE=%WORKAREA%\%SET_NAME%_tbwrkfls\%SET_NAME%.xml

copy %WORKAREA%\Examples\Workshops\Generate_xml\Release\Generate_xml.exe %TBED%\Generate_xml.exe
@echo on
%TBED%\Generate_xml.exe %GLH_FILE%
@echo off

if exist %XML_FILE% goto P1
pause
exit

:P1
if exist "%NTP%\notepad++.exe" goto P2
%TBED%\TBbrowse %XML_FILE%
exit

:P2
"%NTP%\notepad++" %XML_FILE%
exit
