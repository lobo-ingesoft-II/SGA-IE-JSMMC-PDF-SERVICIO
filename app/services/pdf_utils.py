import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import Table, TableStyle
from reportlab.pdfgen import canvas


def crearTablaReportLab_izquierda(data, lienzo:canvas.Canvas, numeroColumnas:int, valorHigh=650, PonerDesdeLimiteAbajo=True, alturaRow=18, anchoCol=3.7 ):
    """_summary_Este metodo es para crear una tabla pasando unos datos y si necesita pasar de pagina en el PDF \n

    Args:\n
        \n\t\t data (array): Array de arrays: cada sub array es una fila 
        \n\t\t lienzo (canvas.Canvas): lienzo canvas
        \n\t\t numeroColumnas (int): numero de columnas de la tabla
        \n\t\t valorHigh (int, optional): valor para desde abajo subir la tabla. Defaults to 650.
        \n\t\t PonerDesdeLimiteAbajo (bool, optional): se pone en 100 la altura de la tabla desde abajo. Defaults to True.
        \n\t\t alturaRow (int, optional): altura de la fila. Defaults to 18.
        \n\t\t anchoCol (float, optional): El ancho de la columna. Defaults to 3.7.\n
       
    """
    high = valorHigh - (len(data) * alturaRow)

    # crear la tabla  y estilizar la tabla
    anchoColumnas = [anchoCol * cm] * numeroColumnas
    table = Table(data, colWidths=anchoColumnas)
    table.setStyle(TableStyle([
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    # Tamaño del PDF
    ancho, alto = A4

    # Ajuste de coordenadas para evitar que la tabla se dibuje fuera de los márgenes
    table.wrapOn(lienzo, ancho, alto)
    if(PonerDesdeLimiteAbajo):
        table.drawOn(lienzo, 30, 100) 
    else:
        table.drawOn(lienzo, 30, high) 
    
    # Cambiar de página si es necesario
    lienzo.showPage()
    return(None)

def crearTablaReportLab_centro(
    data, lienzo:canvas.Canvas, numeroColumnas:int, valorHigh=650,
    PonerDesdeLimiteAbajo=True, alturaRow=18, anchoCol=3.7, cambiar_pagina=False
):
    high = valorHigh - (len(data) * alturaRow)

    ancho, alto = A4
    anchoColumnas = [anchoCol * cm] * numeroColumnas
    table = Table(data, colWidths=anchoColumnas)
    table.setStyle(TableStyle([
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))

    total_ancho_tabla = sum(anchoColumnas)
    x_centrada = (ancho - total_ancho_tabla) / 2

    table.wrapOn(lienzo, ancho, alto)

    # Siempre usa la posición calculada (high), así puedes controlar la altura desde el llamado
    table.drawOn(lienzo, x_centrada, high)

    if cambiar_pagina:
        lienzo.showPage()

    return None