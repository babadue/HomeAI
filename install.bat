@echo off
echo
echo Installing in progress .... please wait...
echo Once finished, the installation will automatically close this window and you should see an icon on your Desktop with HomeAI.
echo 
echo user profile %USERPROFILE%

md "%USERPROFILE%\HomeAI"
set myFolder="%USERPROFILE%\HomeAI"
echo %myFolder%

copy *.py %myFolder%
copy *.bat %myFolder%
copy homeai.ico %myFolder%
call del %myFolder%\install.bat
md %myFolder%\templates
md %myFolder%\config
md %myFolder%\static
copy templates\index.html %myFolder%\templates\
copy config\config.json %myFolder%\config\
copy static\logo.png %myFolder%\static\
cd %myFolder%

call backend_setup.bat
call frontend_setup.bat
call ssl_creation.bat
call icon.bat
