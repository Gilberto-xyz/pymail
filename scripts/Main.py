# Librerias a utilizar
import pandas as pd 
import smtplib
from email.mime.text import MIMEText
from claves import CORREO_EMISOR, CONTRASENA_EMISOR

# Clase para enviar correos electronicos
class  CorreoElectronico:
    # Definimos el constructor de la clase CorreoElectronico que almacena los datos del correo emisor
    def  __init__(self):
        self.correo_emisor = CORREO_EMISOR
        self.contrasena_emisor = CONTRASENA_EMISOR
        self.servidor_smtp = smtplib.SMTP('smtp.gmail.com', 587)
        self.servidor_smtp.starttls()
        
        self.servidor_smtp.login(self.correo_emisor, self.contrasena_emisor)
    
    # Definimos el metodo enviar_correo que contiene el cuerpo del correo
    def enviar_correo(self, correo_receptor, asunto, mensaje):
        
        mensaje = MIMEText(mensaje)
        mensaje['From'] = self.correo_emisor
        mensaje['To'] = correo_receptor
        mensaje['Subject'] = asunto

        self.servidor_smtp.sendmail(self.correo_emisor, correo_receptor, mensaje.as_string())

    # Definimos el metodo cerrar_servidor que cierra la conexion con el servidor
    def cerrar_servidor(self):
        self.servidor_smtp.quit()
        
# Abrimos el archivo csv con los datos de los usuarios
df = pd.read_csv('mailscsv/usuarios.csv')
correos_electronicos = df['correo'].tolist()
nombres = df['nombre'].tolist()

# Enviar los correos
correo = CorreoElectronico()
for correo_receptor in range(len(correos_electronicos)):
    correo.enviar_correo(correos_electronicos[correo_receptor], 'Feliz Jueves', f'Hola {nombres[correo_receptor]}, espero que estes bien. Saludos')
    print(f'Correo enviado a {nombres[correo_receptor]}')
correo.cerrar_servidor()