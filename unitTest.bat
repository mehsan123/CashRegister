set TOOL=%1
set TCF_NAME=%2
set PUBLISH=%3
set SEQ=%4
set BUILD_DIR=%5
set PERMDIR=
echo %PUBLISH%
echo %BUILD_DIR%
echo hi
%TOOL%\\tbini WORKAREA_BASEDIR="%PUBLISH%\"
%TOOL%\\tbini PERMDIR="%PUBLISH%\"

%TOOL%\\contestbed.exe -112a34  %BUILD_DIR%%TCF_NAME%.tcf  

%TOOL%\\Contbrun.exe "%TCF_NAME%" -tcf="%BUILD_DIR%\%SEQ%.tcf" -box=white -regress -quit -unit_publish_to="%PUBLISH%\"

rem %TOOL%\\Contbrun.exe %TCF_NAME%.tcf -tcf="%BUILD_DIR%\%SEQ%.tcf"  -box=white -regress -quit -unit_publish_to="%PUBLISH%"

ldra_unitTest_junit.py "%PUBLISH%\"

LDRA_JACOCO_DYNAMIC.py "%TOOL%\" "%PUBLISH%\"

%TOOL%\\contestbed.exe -32panq  %BUILD_DIR%%TCF_NAME%.tcf -tb_workfiledir="%PUBLISH%\" 
rem %TOOL%\\tbini WORKAREA_BASEDIR=C:\_LDRA_Workarea\1003\
rem %TOOL%\\tbini PERMDIR=C:\_LDRA_Workarea\1003\permdir
rem unitTest.bat "..\..\_tool\1003\" Cashregister D:\AZAjent\vsts-agent-win-x64-2.206.1\_work\1\s\Ehsan\ ut_addProduct D:\AZAjent\vsts-agent-win-x64-2.206.1\_work\1\s\
