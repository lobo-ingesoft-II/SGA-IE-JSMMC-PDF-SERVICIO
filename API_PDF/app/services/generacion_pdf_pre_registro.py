from io import BytesIO

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, cm 
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, PageBreak, Image, Spacer,Paragraph, Table, TableStyle, )
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

from datetime import datetime, timedelta, timezone as datetimeTimeZone

import requests # Para hacer solicitudes HTTP 

# from fastapi.responses import streamingresponse # Para crear respuestas HTTP de PDF 
from app.backend.config import settings


def obtener_prematriculas(id: str):
    # Crear la URL del servidor de la API de pre-registro 
    url_servidor = settings.url_api_pre_registro
    url = url_servidor + f"/pre_registration/{id}"  

    # Realizar la solicitud GET a la API 
    response = requests.get(url)

    # Verificar si la solicitud fue exitosa (código de estado 200)
    
    if response.status_code == 200:
        data = response.json()  # Obtener los datos en formato JSON

        if isinstance(data, dict):  # Si es un diccionario
            return data.get("documento", None)  # Retornar los datos dentro de la clave "data" o None si no existe
        elif not data:  # Si no hay datos, retornar None
            return None
        
        return response.json() # Retornar los datos en formato JSON 
    else:
        return None


# Función para la descarga del PDF
def descarga_reportes(JSONRespuesta:dict):
    """_summary_ 
    \n este metodo es para generar un responseHtml que sea un pdf y se descargue al ingresar a la URL. \n
    """
    # Crear el Objeto PDF, usando BytesIO
    buffer = BytesIO()                          #  buffer espacio temporal de memoria fisica
    lienzo = canvas.Canvas(buffer, pagesize=A4) # pagesize = (21cm, 29.7cm) or (595, 842)

    # Crear el canvas del PDF (CREAR EL PDF)
    try:
        
        generarCanvas_Reporte_prestamo(lienzo, JSONRespuesta)  
        lienzo.save() # guardar el lienzo
        pdf = buffer.getvalue() # obtener el valor del buffer
        buffer.seek(0)  # volver al inicio del buffer
        # buffer.close() # cerrar el buffer
        return buffer
        
      

    except Exception as e:
        print(f"Error al generar el reporte: {e}")
        buffer.close() # Cerrar buffer
        return({"error": e}) # Retornar error
        

#----------------------- CREAR los REPORTES con reportlab ------------------------------------------
# Reporte prestamo 
def generarCanvas_Reporte_prestamo(lienzo:canvas.Canvas, JSONRespuesta:dict):
    ##---------------------------- CREACION ESTILOS -------------------------------------
    # Llamar a los Estilos
    styles = getSampleStyleSheet() # nos da una lista de estilos a escoger de la biblioteca
    

    # Creacion estilo <--  Titulos
    styleHeaderPrincipal = ParagraphStyle(
        'HeaderPrincipal',
        fontName='Helvetica-Bold',
        fontSize=18,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#003366"),
        spaceAfter=6,
        spaceBefore=6,
        leading=22,
    )

    #  Creacion estilo <--  subtítulos
    styleSubHeader_blue = ParagraphStyle(
        'SubHeader',
        fontName='Helvetica-Bold',
        fontSize=12,
        alignment=TA_LEFT,
        textColor=colors.HexColor("#003366"),
        spaceAfter=2,
        spaceBefore=2,
        leading=15,
    )

    styleSubHeader_black = ParagraphStyle(
        'SubHeader',
        fontName='Helvetica-Bold',
        fontSize=12,
        alignment=TA_LEFT,
        textColor=colors.HexColor("#000000"),
        spaceAfter=2,
        spaceBefore=2,
        leading=15,
    )
    # Creacion estilo <-- header tabla
    styleHeaderTable = ParagraphStyle('styleHeaderTable',  
        parent= styles['Heading1'],
        fontSize=10, 
        alignment=1  # Center alignment
    )

    # Creacion estilo <-- header tabla 2 
    styleHeaderTable2 = ParagraphStyle(
        'styleHeaderTable',
        parent=styles['Heading4'],
        fontSize=11,
        fontName='Helvetica-Bold',
        alignment=TA_CENTER,
        textColor=colors.white,
        backColor=colors.HexColor("#003366"),  # Azul oscuro
        spaceAfter=4,
        spaceBefore=4,
        leading=14,
        borderPadding=4,
    )

    # Creacion estilo <-- contenido tabla   
    styleBodyTable = ParagraphStyle('p',  
        parent=styles["BodyText"],
        fontSize=10, 
        alignment= TA_LEFT  # Left alignment
    )

    ##---------------------------- KEYS DE LAS TABLAS -------------------------------------

    keys_info_personal_estudiante = {
        "apellidos": "Apellidos",
        "nombres": "Nombres",
        "tipoDocumento": "Tipo de documento",
        "numeroDocumento": "Número de documento",
        "fechaNacimiento": "Fecha de nacimiento",
        "paisNacimiento": "País de nacimiento",
        "departamentoNacimiento": "Departamento de nacimiento",
        "municipioNacimiento": "Municipio de nacimiento",
        "categoriaSisben": "Categoría Sisbén",
        "subcategoriaSisben": "Subcategoría Sisbén",
        "direccionResidencia": "Dirección de residencia",
        "telefono": "Teléfono",
        "rutaEscolar": "Ruta escolar",
        "seguroMedico": "Seguro médico",
        "discapacidad": "Discapacidad",
        "detalleDiscapacidad": "Detalle de discapacidad",
        "poblacionDesplazada": "Población desplazada",
        "fechaDesplazamiento": "Fecha de desplazamiento",
        "paisResidencia": "País de residencia",
        "departamentoResidencia": "Departamento de residencia",
        "municipioResidencia": "Municipio de residencia",
    }

    # keys Informacion academica
    keys_info_academica = {
        "gradoIngreso": "Grado de ingreso",
        "institucionAnterior": "Institución anterior",
        "municipioAnterior": "Municipio anterior",
        "sede": "Sede"
    }

    # keys Informacion familiar 
    keys_acudiente1 = {
        "acudiente1Parentesco": "Parentesco",
        "acudiente1Apellidos": "Apellidos",
        "acudiente1Nombres": "Nombres",
        "acudiente1CC": "Cédula",
        "acudiente1Celular": "Celular",
        "acudiente1Ocupacion": "Ocupación"
    }

    keys_acudiente2 = {
        "acudiente2Parentesco": "Parentesco",
        "acudiente2Apellidos": "Apellidos",
        "acudiente2Nombres": "Nombres",
        "acudiente2CC": "Cédula",
        "acudiente2Celular": "Celular",
        "acudiente2Ocupacion": "Ocupación"
    }

    heighDocumento = 770  # Altura de las filas del documento
    ancho_pagina, _ = A4  # Obtener el ancho de la página A4
    ##------------------------------  HEADER   ---------------------------------
        #HEADER-titulo

    # Header principal
    header = Paragraph("INSTITUCIÓN EDUCATIVA DEPARTAMENTAL JOSUÉ MANRIQUE", styleHeaderPrincipal)
    w, h = header.wrap(ancho_pagina - 60, heighDocumento)
    header.drawOn(lienzo, 30, heighDocumento)
    heighDocumento -= h

    # Subtítulo
    subheader = Paragraph("INSPECCIÓN DE MAYA. PARATEBUENO", styleSubHeader_blue)
    w, h = subheader.wrap(ancho_pagina - 60, heighDocumento)
    subheader.drawOn(lienzo, 30, heighDocumento)
    heighDocumento -= h

    # Celular
    celular = Paragraph("Celular: 320-4400-124", styleSubHeader_blue)
    w, h = celular.wrap(ancho_pagina - 60, heighDocumento)
    celular.drawOn(lienzo, 30, heighDocumento)
    heighDocumento -= h

    # Correo electrónico
    correo = Paragraph("Correo electrónico: coljosman@hotmail.com", styleSubHeader_blue)
    w, h = correo.wrap(ancho_pagina - 60, heighDocumento)
    correo.drawOn(lienzo, 30, heighDocumento)
    heighDocumento -= h

    # HEADER-hora 
    hora_inicio_reserva = datetime.now(datetimeTimeZone.utc) + timedelta(hours=-5)
    fecha_formateada = hora_inicio_reserva.strftime('%Y-%m-%d %H:%M:%S')
    fecha = Paragraph(f"Fecha de impresión: {fecha_formateada}", styleSubHeader_black)
    w, h = fecha.wrap(ancho_pagina - 60, heighDocumento)
    fecha.drawOn(lienzo, ancho_pagina-250, heighDocumento)
    heighDocumento -= h


    ## ------------------ PRIMERA TABLA (informacion personal estudiante) ----------------------------------
    # Nombre de la tabla
    heighDocumento -= 30  
    nombreTabla = Paragraph("INFORMACIÓN PERSONAL DEL ESTUDIANTE: ", styleSubHeader_black)
    w, h = nombreTabla.wrap(ancho_pagina - 60, heighDocumento)
    nombreTabla.drawOn(lienzo, 40, heighDocumento)
    heighDocumento -= h

    data = []  # Array de datos para la tabla

    # Titulos de la tabla (primera fila); los estilos ya estan creados entonces solo colocar la tabla
    Campo      = Paragraph('Campo', styleHeaderTable2) # Paragraph <-- le da estilo a un texto 
    Dato    = Paragraph('Dato', styleHeaderTable2)
  
    
    data.append([Campo, Dato]) # Pasar datos al (array data)
    highTable = heighDocumento                  # Variable HIGH para saber cuanto mover la tabla relativamente hacia arriba 
    highRow = 15                # Variable para la altura de las filas de la tabla

    # Agregar datos al array de datos (data) de la tabla 
    for key in keys_info_personal_estudiante.keys():
       
        # Obtener el valor del JSON usando la key
        item = JSONRespuesta.get(key, 'No disponible')  # Usar 'No disponible' si la clave no existe
        
        if item == "": # Si el item es una cadena vacía, asignar un valor por defecto
            item = 'No aplica-no rellenado'  # Si el valor es una cadena vacía, asignar un valor por defecto

        # Crear una fila con el campo y el dato dandole estilo 
        row = [Paragraph(keys_info_personal_estudiante.get(key), styleHeaderTable), Paragraph(str(item), styleBodyTable)]
        data.append(row)

        highTable -= highRow  # Reducir el valor de high para la siguiente fila

        if highTable < 360:     # CAMBIAR PAGINA, si se pasa de un numero de datos o high especifico 
            
            # Poner tabla en el CANVAS
            crearTablaReportLab_centro(data, lienzo, 2, valorHigh=highTable , PonerDesdeLimiteAbajo = True, alturaRow= highRow, anchoCol= 8.5 , cambiar_pagina=True)

            # Cambiar el high a 770, ya que alcanzo limite pagina 
            highTable = 770
            heighDocumento = 770
            
            # Limpiar datos del array de datos de la tabla 
            data.clear() 

            # Agregar los (nombres Columnas) a la tabla otra vez 
            data.append([Campo, Dato])
            highTable -= highRow 

    
    # PARA LOS DATOS RESTANTES, si falto dibujar una parte de la tabla
    print("valor high table", highTable)
    crearTablaReportLab_centro(data, lienzo, 2, valorHigh=highTable , PonerDesdeLimiteAbajo = False, alturaRow= highRow, anchoCol= 8.5, cambiar_pagina=False)
    
    # Poner el valor de heighDocumento
    heighDocumento = highTable - 100  # Dejar un espacio de 100 para la siguiente tabla 

    ## ------------------ SEGUNDA  TABLA (informacion Academica) ----------------------------------
    # Nombre de la tabla
    heighDocumento  -= 30
    nombreTabla = Paragraph("INFORMACIÓN ACADÉMICA DEL ESTUDIANTE: ", styleSubHeader_black)
    w, h = nombreTabla.wrap(ancho_pagina - 60, heighDocumento)
    nombreTabla.drawOn(lienzo, 40, heighDocumento)
    heighDocumento -= h
    
    data = []  # Array de datos para la tabla

    # Titulos de la tabla (primera fila); los estilos ya estan creados entonces solo colocar la tabla
    Campo = Paragraph('Campo', styleHeaderTable2)  # Paragraph <-- le da estilo a un texto
    Dato = Paragraph('Dato', styleHeaderTable2)

    data.append([Campo, Dato])  # Pasar datos al (array data)
    highTable = heighDocumento  # Variable HIGH para saber cuanto mover la tabla relativamente hacia arriba
    highRow = 15  # Variable para la altura de las filas de la tabla


    # Agregar datos al array de datos (data) de la tabla
    for key in keys_info_academica.keys():  

        item = JSONRespuesta.get(key, 'No disponible') # Obtener el valor del DIC usando la key

        if item == "":  
            item = 'No aplica-no rellenado'  # Si el valor es una cadena vacía, asignar un valor por defecto

        # Crear una fila con el campo y el dato dandole estilo
        row = [Paragraph(keys_info_academica.get(key), styleHeaderTable), Paragraph(str(item), styleBodyTable)]

        data.append(row)
        highTable -= highRow  # Reducir el valor de high para la siguiente fila

        if highTable < 360:  # CAMBIAR PAGINA, si se pasa de un numero de datos o high especifico

            # Poner tabla en el CANVAS
            crearTablaReportLab_centro(data, lienzo, 2, valorHigh=highTable, PonerDesdeLimiteAbajo=True, alturaRow=highRow, anchoCol=8.5,cambiar_pagina=True) 
            
            # Cambiar el high a 770, ya que alcanzo limite pagina
            highTable = 770
            heighDocumento = 770

            data.clear()   # Limpiar datos del array de datos de la tabla

            # Agregar los (nombres Columnas) a la tabla otra vez
            data.append([Campo, Dato])

    # PARA LOS DATOS RESTANTES, si falto dibujar una parte de la tabla
    crearTablaReportLab_centro(data, lienzo, 2, valorHigh=highTable, PonerDesdeLimiteAbajo=False, alturaRow=highRow, anchoCol=8.5 ,cambiar_pagina=False)

    # Poner el valor de heighDocumento
    heighDocumento = highTable - 80  # Dejar un espacio de 100 para la siguiente tabla 

    ## ------------------ TERCERA TABLA (informacion familiar) ----------------------------------

    # Nombre de la tabla
    heighDocumento -= 30
    nombreTabla = Paragraph("INFORMACIÓN FAMILIAR DEL ESTUDIANTE: (ACUDIENTE 1) ", styleSubHeader_black)
    w, h = nombreTabla.wrap(ancho_pagina - 60, heighDocumento)
    nombreTabla.drawOn(lienzo, 40, heighDocumento)      
    heighDocumento -= h
    data = []  # Array de datos para

    # Titulos de la tabla (primera fila); los estilos ya estan creados entonces solo colocar la tabla   
    Campo = Paragraph('Campo', styleHeaderTable2)  # Paragraph <-- le da estilo a un texto
    Dato = Paragraph('Dato', styleHeaderTable2)

    data.append([Campo, Dato])  # Pasar datos al (array data)
    highTable = heighDocumento  # Variable HIGH para saber cuanto mover la tabla relativamente hacia arriba

    highRow = 15  # Variable para la altura de las filas de la tabla
    # Agregar datos al array de datos (data) de la tabla
    for key in keys_acudiente1.keys():
        item = JSONRespuesta.get(key, 'No disponible')  # Obtener el valor del DIC usando la key

        if item == "":
            item = 'No aplica-no rellenado'  # Si el valor es una cadena vacía, asignar un valor por defecto

        # Crear una fila con el campo y el dato dandole estilo
        row = [Paragraph(keys_acudiente1.get(key), styleHeaderTable), Paragraph(str(item), styleBodyTable)]
        data.append(row)
        highTable -= highRow  # Reducir el valor de high para la siguiente fila

        if highTable < 270:  # CAMBIAR PAGINA, si se pasa de un numero de datos o high especifico
            # Poner tabla en el CANVAS
            crearTablaReportLab_centro(data, lienzo, 2, valorHigh=highTable, PonerDesdeLimiteAbajo=True, alturaRow=highRow, anchoCol=8.5,cambiar_pagina=True)

            # Cambiar el high a 770, ya que alcanzo limite pagina
            highTable = 770
            heighDocumento = 770

            data.clear()  # Limpiar datos del array de datos de la tabla

            # Agregar los (nombres Columnas) a la tabla otra vez
            data.append([Campo, Dato])
    # PARA LOS DATOS RESTANTES, si falto dibujar una parte de la tabla
    crearTablaReportLab_centro(data, lienzo, 2, valorHigh=highTable, PonerDesdeLimiteAbajo=False, alturaRow=highRow, anchoCol=8.5,cambiar_pagina=False)         
    # Poner el valor de heighDocumento
    heighDocumento = highTable - 100  # Dejar un espacio de 100 para la siguiente tabla

    ## ------------------ CUARTA TABLA (informacion familiar 2) ----------------------------------
    lienzo.showPage()  # Cambiar de página para evitar que la tabla se dibuje fuera de los márgenes
    heighDocumento = 770  # Reiniciar la altura del documento para la nueva página

    # Nombre de la tabla
    heighDocumento -= 30
    nombreTabla = Paragraph("INFORMACIÓN FAMILIAR DEL ESTUDIANTE (ACUDIENTE 2): ", styleSubHeader_black)
    w, h = nombreTabla.wrap(ancho_pagina - 60, heighDocumento)

    nombreTabla.drawOn(lienzo, 40, heighDocumento)
    heighDocumento -= h 
    data = []  # Array de datos para
    # Titulos de la tabla (primera fila); los estilos ya estan creados entonces solo colocar la tabla

    Campo = Paragraph('Campo', styleHeaderTable2)  # Paragraph <-- le da estilo a un texto
    Dato = Paragraph('Dato', styleHeaderTable2)

    data.append([Campo, Dato])  # Pasar datos al (array data)

    highTable = heighDocumento  # Variable HIGH para saber cuanto mover la tabla relativamente hacia arriba

    highRow = 15  # Variable para la altura de las filas de la tabla

    # Agregar datos al array de datos (data) de la tabla
    for key in keys_acudiente2.keys():
        item = JSONRespuesta.get(key, 'No disponible')  # Obtener el valor del DIC usando la key

        if item == "":
            item = 'No aplica-no rellenado'  # Si el valor es una cadena vacía, asignar un valor por defecto

        # Crear una fila con el campo y el dato dandole estilo
        row = [Paragraph(keys_acudiente2.get(key), styleHeaderTable), Paragraph(str(item), styleBodyTable)]
        
        data.append(row)
        highTable -= highRow  # Reducir el valor de high para la siguiente fila

        if highTable < 360:  # CAMBIAR PAGINA, si se pasa de un numero de datos o high especifico
            # Poner tabla en el CANVAS
            crearTablaReportLab_centro(data, lienzo, 2, valorHigh=highTable, PonerDesdeLimiteAbajo=True, alturaRow=highRow, anchoCol=8.5,cambiar_pagina=True)

            # Cambiar el high a 770, ya que alcanzo limite pagina
            highTable = 770
            heighDocumento = 770

            data.clear()  # Limpiar datos del array de datos de la tabla

            # Agregar los (nombres Columnas) a la tabla otra vez
            data.append([Campo, Dato])
    # PARA LOS DATOS RESTANTES, si falto dibujar una parte de la tabla
    crearTablaReportLab_centro(data, lienzo, 2, valorHigh=highTable, PonerDesdeLimiteAbajo=False, alturaRow=highRow, anchoCol=8.5,cambiar_pagina=False)

    return None


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