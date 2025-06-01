from io import BytesIO

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import  cm 
from reportlab.platypus import (SimpleDocTemplate, PageBreak, Image, Spacer,Paragraph, Table, TableStyle, )
from reportlab.lib import colors

from datetime import datetime, timedelta, timezone as datetimeTimeZone


#Importar los estilos creados 
from app.services.tabla_styles import (styleHeaderPrincipal, styleSubHeader_blue, styleSubHeader_black,
    styleHeaderTable, styleHeaderTable2, styleBodyTable, styles)

#Importar los diccionarios de los campos de los reportes
from app.services.keysTables import (keys_info_personal_estudiante, keys_info_academica, keys_acudiente1, keys_acudiente2)

# importar la función para crear tablas (propias creadas)
from app.services.pdf_utils import crearTablaReportLab_centro, crearTablaReportLab_izquierda

# Importar la configuración del backend
from app.backend.config import settings



# FUNCIÓN PARA LA DESCARGA DEL PDF 
async def descarga_reportes(JSONRespuesta:dict):
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


# FUNCIÓN CREAR EL PDF EN REPORTLAB 
def generarCanvas_Reporte_prestamo(lienzo:canvas.Canvas, JSONRespuesta:dict):
    ##---------------------------- CREACION ESTILOS -------------------------------------
    # 

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


