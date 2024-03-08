import json
import matplotlib.backends.backend_pdf as pdf
import matplotlib.pyplot as plt
import numpy as np
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PyPDF2 import PdfMerger

# Estimaciones
estimaciones = {
    "Mike": 8,
    "Cecilia": 24,
    "Andres": 8,
    "Cris": 20,
    "Astrid": 8,
    "Alejandro": 12,
    "Luz": 1,
    "Melissa": 20,
    "Sofia": 12,
    "Emi": 8,
    "Hannia": 4,
    "Pablo": 1,
    "Fernanda": 1,
    "Zoe": 4,
    "Miguel": 1
}

# Lecturas reales del archivo JSON
with open('formulariosEnviados.json') as f:
    lecturas = json.load(f)

# Calcular medidas estadísticas descriptivas para enero
lecturas_enero = []
crecimiento_decremento = []
for persona, estimacion in estimaciones.items():
    try:
        # Filtrar solo las fechas de enero
        lecturas_enero_persona = [fecha for fecha in lecturas[persona] if fecha.startswith("2024-02")]
        cantidad_lecturas = len(lecturas_enero_persona)
        porcentaje = min(((cantidad_lecturas - estimacion) / estimacion) * 100, 100)
        # Redondear al múltiplo de 5 más cercano
        porcentaje_redondeado = round(porcentaje / 5) * 5
        lecturas_enero.append(cantidad_lecturas)
        crecimiento_decremento.append(porcentaje_redondeado)
    except KeyError:
        cantidad_lecturas = 0
        porcentaje = min(((cantidad_lecturas - estimacion) / estimacion) * 100, 100)
        # Redondear al múltiplo de 5 más cercano
        porcentaje_redondeado = round(porcentaje / 5) * 5
        lecturas_enero.append(cantidad_lecturas)
        crecimiento_decremento.append(porcentaje_redondeado)

estimaciones_values = [estimaciones[persona] for persona in estimaciones if persona in lecturas]

# Crear el archivo PDF para el informe principal
pdf_output = pdf.PdfPages('informe.pdf')

# Gráfico de barras comparando estimaciones y lecturas en enero
plt.figure(figsize=(10, 18))

# Gráfico 1: Comparación de Estimaciones y Lecturas en Enero
plt.subplot(2, 1, 1)  # Dividir en 1 fila, 2 columnas, y seleccionar el primer subgráfico
personas = [persona for persona in estimaciones if persona in lecturas]
x = np.arange(len(personas))
ancho = 0.35

plt.bar(x - ancho/2, estimaciones_values, width=ancho, label='Devocional Inicial', color='lightcoral',zorder=2)
plt.bar(x + ancho/2, lecturas_enero, width=ancho, label='Devocional Enero', color='skyblue',zorder=2)

plt.ylabel('Cantidad')
plt.title('Comparación de Estimaciones y Lecturas en Enero')
plt.xticks(x, personas, rotation=45)
plt.yticks(np.arange(min(min(estimaciones_values), min(lecturas_enero)), max(max(estimaciones_values), max(lecturas_enero))+1, 1))
plt.grid(axis='y', linestyle='--', linewidth=.5,zorder=1)
plt.grid(axis='x', linestyle='--', linewidth=.5)
plt.legend()

# Gráfico 2: Crecimiento o Decremento
plt.subplot(2, 1, 2)  # Dividir en 1 fila, 2 columnas, y seleccionar el segundo subgráfico
colores = ['green' if p > 0 else 'red' if p < 0 else 'yellow' for p in crecimiento_decremento]
plt.bar(personas, crecimiento_decremento, color=colores, zorder=2)

plt.ylabel('% Crecimiento/Decremento')
plt.title('Comparación de Devocional Inicial/Enero ')
plt.yticks(np.arange(min(crecimiento_decremento), max(crecimiento_decremento)+1, 10))  # Establecer marcas de 5 en 5 en el eje y
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', linewidth=.5, zorder=1)
plt.grid(axis='x', linestyle='--', linewidth=.5)
# Leyenda explicativa
leyenda = {'green': 'Crecimiento', 'red': 'Decremento', 'yellow': 'Mismo'}
plt.legend(handles=[plt.bar(0, 0, color=color, label=leyenda[color]) for color in leyenda], loc='upper right')

# Guardar en PDF
pdf_output.savefig()

# Cerrar el archivo PDF del informe principal
pdf_output.close()

# Gráfico 3: Objetivo Logrado
# plt.subplot(3, 1, 3)
# objetivo_logrado = [1 if lecturas >= estimacion else 0 for lecturas, estimacion in zip(lecturas_enero, estimaciones_values)]
# colores = ['green' if logrado else 'red' for logrado in objetivo_logrado]
# plt.bar(personas, estimaciones_values, color=colores,zorder=2)

# plt.ylabel('Estimación')
# plt.title('Objetivo Logrado')
# plt.xticks(rotation=45)
# plt.grid(axis='y', linestyle='--', linewidth=.5,zorder=1)
# plt.grid(axis='x', linestyle='--', linewidth=.5)

# # Leyenda explicativa
# leyenda = {'green': 'Logrado', 'red': 'No Logrado'}
# plt.legend(handles=[plt.bar(0, 0, color=color, label=leyenda[color]) for color in leyenda], loc='upper right')



# Crear el archivo PDF para la información por usuario
pdf_info_usuario = canvas.Canvas("informacion_por_usuario.pdf", pagesize=letter)
pdf_info_usuario.drawString(100, 750, "Información por Usuario:")
pdf_info_usuario.drawString(100, 730, "")

line_height = 100  # Espacio entre líneas
initial_y = 700  # Posición inicial en el eje y
max_y = 50  # Posición y máxima antes de pasar a la siguiente página

y_position = initial_y  # Inicializar la posición vertical actual

for i, (persona, estimacion) in enumerate(estimaciones.items(), start=1):
    try:
        # Filtrar solo las fechas de enero
        lecturas_enero_persona = [fecha for fecha in lecturas[persona] if fecha.startswith("2024-01")]
        cantidad_lecturas = len(lecturas_enero_persona)
        porcentaje = ((cantidad_lecturas - estimacion) / estimacion) * 100
        if y_position < max_y:
            pdf_info_usuario.showPage()  # Agregar nueva página si el espacio es insuficiente
            pdf_info_usuario.drawString(100, 750, "Información por Usuario:")
            pdf_info_usuario.drawString(100, 730, "")
            y_position = initial_y  # Restablecer la posición vertical al inicio de la página
        pdf_info_usuario.drawString(100, y_position, f'{persona}:')
        pdf_info_usuario.drawString(120, y_position - 20, f'  - Estimación: {estimacion}')
        pdf_info_usuario.drawString(120, y_position - 40, f'  - Cantidad en Enero: {cantidad_lecturas}')
        pdf_info_usuario.drawString(120, y_position - 60, f'  - Porcentaje de Crecimiento/Decremento: {porcentaje:.2f}%')
        pdf_info_usuario.drawString(100, y_position - 80, "")
        y_position -= line_height  # Mover la posición vertical hacia arriba para la próxima línea de texto
    except KeyError:
        if y_position < max_y:
            pdf_info_usuario.showPage()  # Agregar nueva página si el espacio es insuficiente
            pdf_info_usuario.drawString(100, 750, "Información por Usuario:")
            pdf_info_usuario.drawString(100, 730, "")
            y_position = initial_y  # Restablecer la posición vertical al inicio de la página
        pdf_info_usuario.drawString(100, y_position, f'{persona}:')
        pdf_info_usuario.drawString(120, y_position - 20, f'  - Estimación: {estimacion}')
        pdf_info_usuario.drawString(120, y_position - 40, '  - Cantidad en Enero: 0')
        pdf_info_usuario.drawString(120, y_position - 60, '  - Porcentaje de Crecimiento/Decremento: No se puede calcular')
        pdf_info_usuario.drawString(100, y_position - 80, "")
        y_position -= line_height  # Mover la posición vertical hacia arriba para la próxima línea de texto

pdf_info_usuario.save()



# Fusionar archivos PDF
pdf_merger = PdfMerger()

# Agregar informe principal
pdf_merger.append('informe.pdf')

# Agregar información por usuario
pdf_merger.append('informacion_por_usuario.pdf')

# Guardar archivo PDF fusionado
with open('informe_final.pdf', 'wb') as output:
    pdf_merger.write(output)
