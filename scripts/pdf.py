from reportlab.pdfgen import canvas

# Creamos el PDF dinamico
c = canvas.Canvas(f'Bienvenida.pdf')
# Mensaje de bienvenida x, y, mensaje
c.drawString(50, 800, f'Hola, Bienvenido')
c.drawString(50, 750, f'¡Estoy muy emocionado de darte la bienvenida al equipo!')
c.drawString(50, 700, f'Sé que comenzar un nuevo trabajo puede ser abrumador')
c.drawString(50, 650, f' Estoy emocionado de ver lo que logras en tu nuevo rol. ¡Bienvenido al equipo!') 
        
c.save()