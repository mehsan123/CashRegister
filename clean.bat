if exist inszt_*.c del /F inszt_*.c
if exist *.cerr del /F *.cerr
if exist *.o del /F *.o
if exist *.d del /F *.d
if exist Cashregister.exe del /F Cashregister.exe

if errorlevel=1 pause
