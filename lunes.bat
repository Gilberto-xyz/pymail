:: Archivo bat que ejecuta tras la programacion de tareas de windows
@echo off

:: Mensaje informativo
echo "Ejecutando el envio de correos"

:: Ejecucion del script de python (instruccion para windows)
python C:\Users\G\Desktop\pymail\scripts\TienesUnMensaje.py

echo "Envio de correos finalizado"