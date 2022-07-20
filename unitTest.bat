set TOOL=%1
set TCF_NAME=%2
set PUBLISH=%3
set SEQ=%4
set BUILD_DIR=%5
echo %PUBLISH%
echo %BUILD_DIR%
echo hi

%TOOL%\\contestbed.exe -112a34  %BUILD_DIR%%TCF_NAME%.tcf -tb_workfiledir="%PUBLISH%" 

%TOOL%\\Contbrun.exe %TCF_NAME%.tcf -tcf=%BUILD_DIR%\\%SEQ%.tcf -box=white -regress -quit -unit_publish_to="%PUBLISH%" 
rem %TOOL%\\Contbrun.exe %TCF_NAME%.tcf -tcf="%BUILD_DIR%\%SEQ%.tcf" -unit_publish_to="%PUBLISH%" -box=black -regress -quit 

ldra_unitTest_junit.py %PUBLISH%
