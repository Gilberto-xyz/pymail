import claves
import smtplib
from email.message import EmailMessage
from reportlab.pdfgen import canvas
import pandas as pd

CORREO_EMISOR = claves.CORREO_EMISOR
CORREO_CONTRASENA = claves.CONTRASENA_EMISOR

# contactos = csv
df = pd.read_csv('C:/Users/G/Desktop/pymail/mailscsv/usuarios.csv')
correos_usuarios = df['correo'].tolist()
nombres = df['nombre'].tolist()



mensaje = EmailMessage()
mensaje['Subject'] = 'Prueba de correo'
mensaje['From'] = CORREO_EMISOR
# for correo_receptor in range(len(correos_usuarios)):
mensaje['To'] = 'not.giiilberto@gmail.com'
mensaje.set_content(f'PDF adjunto')
# mensaje['To'] = correos_receptor
# mensaje.set_content('PDF adjunto')
lienzo = canvas.Canvas(f'test.pdf')
lienzo.drawString(50, 800, f'Hola, {nombres} Bienvenido')
lienzo.drawString(50, 750, f'¡Estoy muy emocionado de darte la bienvenida al equipo!')
lienzo.drawString(50, 725, f'Sé que comenzar un nuevo trabajo puede ser abrumador,')
lienzo.drawString(50, 700, f'Estoy emocionado de ver lo que logras en tu nuevo rol. ¡Bienvenido al equipo!') 
lienzo.drawString(50, 600, f'Te enviaremos informacion mediante {CORREO_EMISOR}') 
lienzo.drawString(50, 575, f'asi que no olvides revisar tu correo con el que te registraste: {mensaje["To"]}') 
lienzo.save()
archivo_pdf = 'test.pdf'
# archivo_pdf = 'Bienvenida.pdf'

for archivo in archivo_pdf:
    with open(archivo_pdf, 'rb') as pdf:
        archivo_datos = pdf.read()
        archivo_nombre = pdf.name
    mensaje.add_attachment(archivo_datos, maintype='application', subtype='octet-stream', filename=archivo_nombre)

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(CORREO_EMISOR, CORREO_CONTRASENA)
    smtp.send_message(mensaje)
    print('Correo enviado')
