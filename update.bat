set myFolder="%USERPROFILE%\HomeAI"
echo %myFolder%

copy *.py %myFolder%
copy *.bat %myFolder%
copy homeai.ico %myFolder%
call del %myFolder%\install.bat
call del %myFolder%\update.bat
call del %myFolder%\Msg_Exchange_Class.py
copy templates\index.html %myFolder%\templates\
copy static\logo.png %myFolder%\static\
call backend_update.bat
call frontend_update.bat