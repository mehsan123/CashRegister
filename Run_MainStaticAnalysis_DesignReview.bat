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


rem Copy the updated executable to the LDRA_Toolsuite folder
rem ========================================================
set CONFIG_DIR=%PRJ_ROOT%\Configuration
copy %CONFIG_DIR%\Userstandards_combined.exe %TBED%\Userstandards_combined.exe


rem Delete the existing set and work directory
rem ==========================================
start "ldra" /wait /min %TBED%\%TOOL% /delete_set=%PRJ_NAME%
if exist %WORK_DIR% rmdir /s /q %WORK_DIR%


rem Set up necessary testbed.ini options in the default Testbed section
rem These options will be set for all sets
rem Any project specific options will be saved in the project tcf file
rem ===================================================================
start "ldra" /wait /min %TBED%\TBini COMPILER_SELECTED="%COMPILER%"
rem Enable integration with Subversion and add version number to reports
start "ldra" /wait /min %TBED%\TBini CM_TOOL_SELECTED=Subversion
start "ldra" /wait /min %TBED%\TBini CM_ADD_VERSION_TO_REPORTS=TRUE
rem When reporting to support, just create a text file, don't open the email tool
rem start "ldra" /wait /min %TBED%\TBini REDIRECT_MAILTO=TRUE
rem Hungarian and user rules require a customised executable
start "ldra" /wait /min %TBED%\TBini USER_STANDARDS_GENERATOR=%TBED%\Userstandards_combined.exe
rem Only analyze the rules defined in the standard (speeds things up a bit)
start "ldra" /wait /min %TBED%\TBini ENABLE_ALL_STANDARDS=FALSE
rem Allow in TBvision option to view code review by violations (activate context menu entry)
start "ldra" /wait /min %TBED%\TBini CODE_REVIEW_CONTEXT_MENU=7
rem Force tool to use custom cpen.dat and creport.dat
start "ldra" /wait /min %TBED%\TBini CPENFILE=%CONFIG_DIR%\cpen.dat
start "ldra" /wait /min %TBED%\TBini CREPFILE=%CONFIG_DIR%\creport.dat
rem Force tool to use custom metpen.dat
start "ldra" /wait /min %TBED%\TBini METFILE=%CONFIG_DIR%\metpen.dat
rem Always generate individual files when there are less than 32 files in the set
start "ldra" /wait /min %TBED%\TBini FILE_LIMIT=32


rem Run the Main Static, Complexity Analysis, Data Flow, Information Flow
rem =====================================================================
start "ldra" /wait /min %TBED%\%TOOL% %SRC_FILES% /112a345q

rem Generate a Test Manager Report
rem ==============================
start "ldra" /wait /min %TBED%\%TOOL% %SRC_FILES% /generate_overview_rep

rem Open the Test Manager Report
rem ============================
if exist %WORK_DIR%\%PRJ_NAME%.ovs.htm %TBED%\TBbrowse %WORK_DIR%\%PRJ_NAME%.ovs.htm
