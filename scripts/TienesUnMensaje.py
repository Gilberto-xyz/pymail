import claves  # Claves de correo
import smtplib  # Protocolo de transferencia simple de correo
import pandas as pd  # Libreria para manipular datos
from datetime import datetime  # Libreria para manipular fechas
from reportlab.pdfgen import canvas  # Libreria para crear PDFs
# Libreria para crear mensajes de correo oriendato a PDF
from email.message import EmailMessage


class Usuario:
    def __init__(self, nombre, correo, nacimiento):
        self.nombre = nombre
        self.correo = correo
        self.nacimiento = nacimiento

    def __str__(self):
        return f'{self.nombre} ({self.correo})'

    def cumpleanos_hoy(self):
        hoy = datetime.now().date()
        return self.nacimiento.day == hoy.day and self.nacimiento.month == hoy.month


class CorreoElectronico:
    def __init__(self):
        self.correo_emisor = claves.CORREO_EMISOR
        self.contrasena_emisor = claves.CONTRASENA_EMISOR
        self.servidor_smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        self.servidor_smtp.login(self.correo_emisor, self.contrasena_emisor)

    def enviar_correo(self, correo_receptor, asunto, cuerpo, adjunto=None):
        mensaje = EmailMessage()
        mensaje['From'] = self.correo_emisor
        mensaje['To'] = correo_receptor
        mensaje['Subject'] = asunto
        mensaje.set_content(cuerpo)

        # Si se adjunta un archivo, enviar el pdf 
        # Si no, enviar el correo sin adjunto (bug de que al cumpleañero se le enviaba el correo de bienvenida xd)
        if adjunto is not None:
            lienzo = canvas.Canvas(f'Nuevo ingreso.pdf')
            lienzo.drawString(50, 800, f'Hola, Bienvenido')
            lienzo.drawString(
                50, 750, f'¡Estoy muy emocionado de incluirte al equipo!')
            lienzo.drawString(
                50, 725, f'Sé que comenzar un nuevo trabajo puede ser abrumador,')
            lienzo.drawString(
                50, 600, f'Te enviaremos informacion mediante {self.correo_emisor}')
            lienzo.drawString(
                50, 575, f'asi que no olvides revisar tu correo con el que te registraste: {mensaje["To"]}')
            lienzo.save()
            archivo_pdf = 'Nuevo ingreso.pdf'
            for archivo in archivo_pdf:
                with open(archivo_pdf, 'rb') as pdf:
                    archivo_datos = pdf.read()
                    archivo_nombre = pdf.name
                mensaje.add_attachment(archivo_datos, maintype='application',
                                    subtype='octet-stream', filename=archivo_nombre)

        self.servidor_smtp.send_message(mensaje)

    def cerrar_servidor(self):
        self.servidor_smtp.quit()

class CorreosCSV:
    def __init__(self, archivo_csv):
        self.usuarios = []
        self.cargar_usuarios_desde_csv(archivo_csv)

    def cargar_usuarios_desde_csv(self, archivo_csv):
        df = pd.read_csv(archivo_csv)
        df['nacimiento'] = pd.to_datetime(df['nacimiento'])
        for index, row in df.iterrows():
            usuario = Usuario(row['nombre'], row['correo'], row['nacimiento'])
            self.usuarios.append(usuario)

    def enviar_correos_bienvenida(self):
        correo = CorreoElectronico()

        for usuario in self.usuarios:
            # Si el usuario cumple años, enviar correo de cumpleaños
            if usuario.cumpleanos_hoy():
                asunto = 'Feliz cumpleaños!'
                mensaje = ' '
                print(f'Enviando correo de Feliz cumpleaños a {usuario}')
                mensaje = EmailMessage()

                # Funciona pero manda el correo en texto plano
                mensaje.set_content('Feliz cumpleaños!')
                mensaje.add_alternative("""\
                <!DOCTYPE html>
<head>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
</head>
<body>
    <div class="container">
        <div class="row">
            <div class="col-md-12 text-center">
                <h1>¡Feliz Dia!</h1>
                <p>Hoy celebramos tu vida y todo lo que has logrado hasta ahora. Eres una persona increíblemente talentosa y valiente que ha superado muchos obstáculos en su camino. Espero que este nuevo año de vida te traiga muchas alegrías y éxitos.</p>
                <img src="https://i0.wp.com/acegif.com/wp-content/gif/hapby-cat-32.gif" alt="cute kitten gif" height=500px>
            </div>
        </div>
    </div>
</body>
</html>""", subtype='html')
                correo.enviar_correo(usuario.correo, asunto,
                                     cuerpo=mensaje, adjunto=None)
            # Si el usuario no cumple años, enviar correo de bienvenida
            else:
                asunto = 'Bienvenido a la empresa'
                mensaje = '''Hola, ¡Bienvenido!\nEn el archivo adjunto encontrarás información importante sobre la empresa.'''
                adjuntos = 'Nuevo ingreso.pdf'
                print(f'Enviando correo de bienvenida a {usuario}')
                correo.enviar_correo(usuario.correo, asunto, cuerpo=mensaje, adjunto=adjuntos)
        correo.cerrar_servidor()


# Ejecutar desde la terminal
correos_csv = CorreosCSV('C:/Users/G/Desktop/pymail/mailscsv/usuarios.csv')
correos_csv.enviar_correos_bienvenida()
