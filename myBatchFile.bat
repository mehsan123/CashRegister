echo "Hello World!!!!"
set AGENT_HOME=C:\agent\_work
set PATH=%AGENT_HOME%\LDRA\LDRA_Toolsuite\;%PATH%

copy C:\ProgramData\LDRA\testbed.ini 

set TESTBED=%CD%
tbini PERMDIR=%AGENT_HOME%\LDRA\LDRA_Workarea\PERMDIR
tbini WORKAREA_BASEDIR=%AGENT_HOME%\LDRA\LDRA_WORKAREA\
contestbed.exe -11q cashregister.tcf -generate_code_review

set GLH_FILE=%WORK%\%PRJ%_tbwrkfls\%PRJ%.glh

set XML_FILE=%WORK%\%PRJ%_tbwrkfls\%PRJ%.xml




if exist %XML_FILE% %XML_FILE%

integration_util /arg=3 /1=Result.xml /2=%AGENT_HOME%\LDRA\LDRA_Workarea\Cashregister_5_tbwrkfls\Cashregister_5.glh /3=
