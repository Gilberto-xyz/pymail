# Librerias a utilizar
import pandas as pd

import smtplib
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from reportlab.pdfgen import canvas

import claves
from datetime import datetime

# Clase para enviar correos electronicos
class CorreoElectronico:
    # Definimos el constructor de la clase CorreoElectronico que almacena los datos del correo emisor
    def __init__(self):
        self.correo_emisor = claves.CORREO_EMISOR
        self.contrasena_emisor = claves.CONTRASENA_EMISOR
        self.servidor_smtp = smtplib.SMTP('smtp.gmail.com', 587)
        self.servidor_smtp.starttls()

        self.servidor_smtp.login(self.correo_emisor, self.contrasena_emisor)

    # Definimos el metodo enviar_correo que contiene el cuerpo del correo
    def enviar_correo(self, correo_receptor, asunto, cuerpo):
        # Aqui cambiamos el MIMEText por MIMEMultipart para enviar correos con HTML
        mensaje = MIMEMultipart(cuerpo)
        mensaje['From'] = self.correo_emisor
        mensaje['To'] = correo_receptor
        mensaje['Subject'] = asunto

        # Envio de archivos adjuntos PDF
        mensaje.attach(MIMEText(cuerpo, 'plain'))

        self.servidor_smtp.sendmail(
            self.correo_emisor, correo_receptor, mensaje.as_string())

    # Definimos el metodo cerrar_servidor que cierra la conexion con el servidor
    def cerrar_servidor(self):
        self.servidor_smtp.quit()

# Metodo para Correos masivos guardados en un CSV
# Abrimos el archivo csv con los datos de los usuarios
class CorreosCSV:
    def __init__(self, archivo_csv):
        self.correos_electronicos = []
        self.nombres = []

        df = pd.read_csv(archivo_csv)

        # obtenemos la fecha de nacimiento del usuario y la pasamos a formato datetime
        df['nacimiento'] = pd.to_datetime(df['nacimiento'])

        # f'El usuario {df_filtrado["nombre"].tolist()} cumple años hoy')
        self.correos_electronicos = df['correo'].tolist()
        self.nombres = df['nombre'].tolist()

    def enviar_correos(self, asunto, mensaje):
        correo = CorreoElectronico()
        for correo_receptor in range(len(self.correos_electronicos)):
            correo.enviar_correo(
                self.correos_electronicos[correo_receptor], asunto, mensaje)
            print(f'Correo enviado a {self.nombres[correo_receptor]}')
        correo.cerrar_servidor()



# correos_automaticos = CorreosCSV(
#     'C:/Users/G/Desktop/pymail/mailscsv/usuarios.csv')
# correos_automaticos.enviar_correos()
