@echo off
setlocal enableextensions enabledelayedexpansion

rem +---------------------------------------------------------+
rem | Author : M.W.Richardson                                 |
rem | Date   : 20/06/2016                                     |
rem |                                                         |
rem | Searches for all nested source and header files         |
rem | It then creates a .tcf file                             |
rem |                                                         |
rem | Copyright : (c) 2016 Liverpool Data Research Associates |
rem +---------------------------------------------------------+

rem Create tcf file
rem ===============
echo.

set SET_NAME=Cashregister_5
set SET_TCF="%CD%\%SET_NAME%.tcf"
set NTP=%PROGRAMFILES(X86)%\Notepad++
set CFG="%CD%\Configuration"

echo # Begin Testbed Set> %SET_TCF%
echo. >> %SET_TCF%
echo    SET_TYPE = SYSTEM>> %SET_TCF%
echo    SET_NAME = %SET_NAME%>> %SET_TCF%
echo    GENERATED_BY = SCRIPT>> %SET_TCF%
echo. >> %SET_TCF%
echo    # Begin Source Files>> %SET_TCF%
echo. >> %SET_TCF%

rem For each c file, except inszt ones
rem ==================================
for /r %%f in (*.c) do (
  set file_name=%%~nf
  rem If the file starts with inszt_ then ignore it
  set "value=!file_name:inszt_=!"
  if "!value!" == "!file_name!" (
    echo       File = %%f >> %SET_TCF%
  )
)
echo. >> %SET_TCF%
echo    # End Source Files>> %SET_TCF%
echo. >> %SET_TCF%
echo    # Begin Sysearch Include File Entries>> %SET_TCF%
echo. >> %SET_TCF%
rem For each folder containing a .h file
rem ====================================
if exist %cd%\*.h echo       SearchPath = %cd% >> %SET_TCF%
for /D /r %%d in (*) do (
  if exist %%d\*.h echo       SearchPath = %%d >> %SET_TCF%
)
echo. >> %SET_TCF%
echo    # End Sysearch Include File Entries>> %SET_TCF%
echo. >> %SET_TCF%
echo    # Begin Sysppvar Preprocessor Macros>> %SET_TCF%
echo. >> %SET_TCF%
echo       MacroEntry = TUTORIAL 1 >> %SET_TCF%
echo. >> %SET_TCF%
echo    # End Sysppvar Preprocessor Macros>> %SET_TCF%
echo. >> %SET_TCF%
echo # End Testbed Set>> %SET_TCF%
echo. >> %SET_TCF%
echo # Begin Options>> %SET_TCF%
echo. >> %SET_TCF%
echo. $ Options for static analysis>> %SET_TCF%
echo    include = True>> %SET_TCF%
echo    open_all_includes = False>> %SET_TCF%
echo    shorten = True>> %SET_TCF%
echo    cstandards_model = MISRA-C:2012/AMD1>> %SET_TCF%
echo    cexternal_standard = MISRA-C:2012/AMD1>> %SET_TCF%
echo. >> %SET_TCF%
echo. $ Options for dynamic analysis>> %SET_TCF%
echo    nb_substitute_source = True>> %SET_TCF%
echo    nb_mechanism = makefile>> %SET_TCF%
echo    nb_makefile_name = Cashregister.mak>> %SET_TCF%
echo    nb_start_in_dir = %CD%\Src\>> %SET_TCF%
echo    nb_makefile_command = mingw32-make -f "$(Makefile)" $(MakeGoal) $(MakeArgs)>> %SET_TCF%
rem echo. $ Options for custom coverage reporting>> %SET_TCF%
rem echo    dyn_scan_option = 10>> %SET_TCF%
rem echo    dyn_scan_custom_data = 8 1 1 1 0 1 1 1 1>> %SET_TCF%
rem echo    dyn_scan_custom_coverage = 5 60 100 100 60 100>> %SET_TCF%
rem echo    dyn_scan_current_coverage = 5 100 100 100 100 100>> %SET_TCF%
echo. >> %SET_TCF%
echo # End Options>> %SET_TCF%
echo.

if exist %SET_TCF% goto P1
pause
exit

:P1
if exist "%NTP%\notepad++.exe" goto P2
%TBED%\TBbrowse %SET_TCF%
exit

:P2
"%NTP%\notepad++" %SET_TCF%
exit

