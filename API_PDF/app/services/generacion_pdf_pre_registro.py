from io import BytesIO

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, cm 
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, PageBreak, Image, Spacer,Paragraph, Table, TableStyle, )
from reportlab.lib import colors

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
    
    # Creacion estilo <-- header tabla
    styleHeaderTable = ParagraphStyle('styleHeaderTable',  
        parent= styles['Heading1'],
        fontSize=10, 
        alignment=1  # Center alignment
    )

    # Creacion estilo <-- contenido tabla   
    styleBodyTable = ParagraphStyle('p',  
        parent=styles["BodyText"],
        fontSize=7, 
        alignment=1  # Center alignment
    )

    ##---------------------------- KEYS DE LAS TABLAS -------------------------------------

    keys_info_personal_estudiante = [
    "apellidos",
    "nombres",
    "tipoDocumento",
    "numeroDocumento",          # Representa el número del documento
    "fechaNacimiento",          # mm/dd/yyyy
    "paisNacimiento",           # COLOMBIA
    "departamentoNacimiento",
    "municipioNacimiento",
    "categoriaSisben",
    "subcategoriaSisben",
    "direccionResidencia",
    "telefono",                 # Teléfono / Celular
    "rutaEscolar",
    "seguroMedico",
    "discapacidad",
    "detalleDiscapacidad",      # Puede ir como parte de discapacidad
    "poblacionDesplazada",
    "fechaDesplazamiento",      # Puede omitirse si no aplica
    "paisResidencia",           # COLOMBIA
    "departamentoResidencia",
    "municipioResidencia"]

    keys_info_academica = [
    "gradoIngreso",
    "institucionAnterior",
    "municipioAnterior",
    "sede"
    ]

    # keys Informacion familiar 
    keys_acudiente1 = [
    "acudiente1Parentesco",
    "acudiente1Apellidos",
    "acudiente1Nombres",
    "acudiente1CC",
    "acudiente1Celular",
    "acudiente1Ocupacion"
    ]

    keys_acudiente2 = [
        "acudiente2Parentesco",
        "acudiente2Apellidos",
        "acudiente2Nombres",
        "acudiente2CC",
        "acudiente2Celular",
        "acudiente2Ocupacion"
    ]


    ##------------------------------  HEADER   ---------------------------------
        #HEADER-titulo
    lienzo.setLineWidth(.3)
    lienzo.setFont('Helvetica', 22)
            # X desde el lad IZQ cuanto mover a la DER
            # y desde al lad ABJ cuanto mover ARRIBA
        # header-subtitulo
    lienzo.drawString(x=30, y=750,text='INSTITUCION EDUCATIVA DEPARTAMENTAL JOSUE MANRIQUE')
    lienzo.setFont('Helvetica', 12)


    lienzo.drawString(30, 730, "Reporte PRESTAMOS")

        # HEADER-hora
    hora_inicio_reserva = datetime.now(datetimeTimeZone.utc) + timedelta(hours=-5) # Ajustar a la zona horaria de Colombia (UTC-5)
    fecha_formateada = hora_inicio_reserva.strftime('%Y-%m-%d %H:%M:%S')           # Formatear la fecha y hora
    
    lienzo.setFont("Helvetica-Bold", 12)
    lienzo.drawString(350, 750, f"Fecha Reporte: {fecha_formateada}")
    
 
    ## ------------------ PRIMERA TABLA (informacion personal estudiante) ----------------------------------
    data = []  # Array de datos para la tabla

    # TITULOS DE LA TABLA (primera fila); los estilos ya estan creados entonces solo colocar la tabla
    Campo      = Paragraph('Campo', styleHeaderTable) # Paragraph <-- le da estilo a un texto 
    Dato    = Paragraph('Dato', styleHeaderTable)
  
    
    data.append([Campo, Dato]) # Pasar datos al (array data)
    highBeforeTable = 700           # # Variable HIGH para saber el inicio de la tabla, desde donde se dibuja la tabla
    highTable = 700                 # Variable HIGH para saber cuanto mover la tabla relativamente hacia arriba 
    highRow = 18                # Variable para la altura de las filas de la tabla

    # Agregar datos al array de datos (data) de la tabla 
    for key in keys_info_personal_estudiante:
       
        # Obtener el valor del JSON usando la key
        item = JSONRespuesta.get(key, 'No disponible')  # Usar 'No disponible' si la clave no existe

        # Crear una fila con el campo y el dato dandole estilo 
        row = [Paragraph(key, styleHeaderTable), Paragraph(str(item), styleBodyTable)]
        data.append(row)

        highTable -= highRow  # Reducir el valor de high para la siguiente fila
        data.append(row) 


        if highTable < 360:     # CAMBIAR PAGINA, si se pasa de un numero de datos o high especifico 
            
            # Poner tabla en el CANVAS
            crearTablaReportLab(data, lienzo, 5, valorHigh= 700, PonerDesdeLimiteAbajo = True, alturaRow= highRow, anchoCol= 3.7)

            # Cambiar el high a 750, ya que alcanzo limite pagina 
            high = 750
            
            # Limpiar datos del array de datos de la tabla 
            data.clear() 

            # Agregar los (nombres Columnas) a la tabla otra vez 
            data.append([Campo, Dato])

    
    # PARA LOS DATOS RESTANTES, si falto dibujar una parte de la tabla
    crearTablaReportLab(data, lienzo, 5, valorHigh=600, PonerDesdeLimiteAbajo = False, alturaRow= 20, anchoCol= 3.7)

    ##------------------ CUANTOS PRESTAMOS ----------------------------------
    lienzo.setFont('Helvetica', 10)
    lienzo.drawString(x=30, y=750,text=f'''1.5  ¡TOTAL PRESTAMOS, CON FILTROS!, ¿Cuántos prestamos hay?:''')
    lienzo.setFont('Helvetica-Bold', 15)
    lienzo.drawString(x=370, y=750,text=f'''fdfd ''')
    lienzo.setFont('Helvetica', 10)
    lienzo.drawString(x=30, y=735,text='---------------------------------------------------------------------------------------------------------------------------')

    return None


def crearTablaReportLab(data, lienzo:canvas.Canvas, numeroColumnas:int, valorHigh=650, PonerDesdeLimiteAbajo=True, alturaRow=18, anchoCol=3.7 ):
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

