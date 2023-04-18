# Libreria para enviar correos
import smtplib
from email.mime.text import MIMEText

# Objeto SMTP y conexion al servidor de Gmail
servidor = smtplib.SMTP('smtp.gmail.com', 587)
servidor.starttls()
servidor.login('not.giiilberto@gmail.com', 'contraseña')


# Mensaje a enviar con MIMEtext

mensaje = MIMEText('Hola, este es un mensaje de prueba')
mensaje['Subject'] = 'Prueba'
mensaje['From'] = 'not.giiilberto@gmail.com'
mensaje['To'] = 'gilberto.nava.marcos@protonmail.com'

# Envio del mensaje
servidor.sendmail('not.giiilberto@gmail.com','gilberto.nava.marcos@protonmail.com', mensaje.as_string())


