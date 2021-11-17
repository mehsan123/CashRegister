rem Configure variables that are likely to change
rem =============================================
set PRJ_NAME=Cashregister
set COMPILER=MinGW200 GCC C/C++ v3.2
set TBED="C:\_LDRA_Toolsuite\988_RC1"
set WORKAREA_BASEDIR="C:\_LDRA_Workarea\988_RC1"
set TOOL=contestbed

rem Configure relative paths 
rem ========================
set PRJ_ROOT="%CD%"
set SRC_FILES=%PRJ_ROOT%\%PRJ_NAME%.tcf
set WORK_DIR=%WORKAREA_BASEDIR%\%PRJ_NAME%_tbwrkfls

rem Delete the existing set and work directory
rem ==========================================
start "ldra" /wait /min %TBED%\%TOOL% /delete_set=%PRJ_NAME%
if exist %WORK_DIR% rmdir /s /q %WORK_DIR%

rem Set up necessary testbed.ini options in the default Testbed section
rem ===================================================================
start "ldra" /wait /min %TBED%\TBini COMPILER_SELECTED="%COMPILER%"
start "ldra" /wait /min %TBED%\TBini CM_TOOL_SELECTED=Subversion
start "ldra" /wait /min %TBED%\TBini CM_ADD_VERSION_TO_REPORTS=TRUE
rem start "ldra" /wait /min %TBED%\TBini REDIRECT_MAILTO=TRUE

rem Run just the Main Static analysis
rem =================================
start "ldra" /wait /min %TBED%\%TOOL% %SRC_FILES% /11aq

