set TOOL=%1
set TCF_NAME=%2
set PUBLISH=%3
set SEQ=%4
set BUILD_DIR=%5

echo hi

%TOOL%\\Contbrun.exe %BUILD_DIR%%TCF_NAME% -seq=%BUILD_DIR%\\%SEQ%.tcf -unit_publish_to=%PUBLISH% -box=black -regress -quit
ldra_unitTest_junit.py %PUBLISH%\\%SEQ%\\%SEQ%.thr.txt
