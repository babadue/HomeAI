set myFolder="%USERPROFILE%\HomeAI"
echo %myFolder%

copy *.py %myFolder%
copy *.bat %myFolder%
copy homeai.ico %myFolder%
call del %myFolder%\install.bat
call del %myFolder%\update.bat
copy templates\index.html %myFolder%\templates\
copy static\logo.png %myFolder%\static\