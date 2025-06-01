import os
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, cm 
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, PageBreak, Image, Spacer,
Paragraph, Table, TableStyle, )
from reportlab.lib import colors
from datetime import datetime, timedelta
import requests
from app.backend.config import settings


def obtener_prematriculas(id: str):
    # Crear la URL del servidor de la API de pre-registro 
    url_servidor = settings.url_api_pre_registro
    url = url_servidor + f"/pre_registration/{id}"  

    # Realizar la solicitud GET a la API 
    response = requests.get(url)

    # Verificar si la solicitud fue exitosa (código de estado 200)
    
    if response.status_code == 200:
        return response.json() # Retornar los datos en formato JSON 
    else:
        return None


# # Función para la descarga del PDF
# def descarga_reportes(request,nombreArchivoReporte:str,numeroReporte:int ):
#     """_summary_ 
#     \n este metodo es para generar un responseHtml que sea un pdf y se descargue al ingresar a la URL. \n
#     Args:
#         nombreArchivoReporte (str): Pasado por la URL, es el nombre que se le dara al archivo pdf. \n
#         numeroReporte (int): Pasado por la URL: 
#         \n\t\t 1 <-- Reporte de prestamos. 
#         \n\t\t 2 <-- Reporte de eventos. 
#         \n\t\t 3 <-- Reporte de asistencia. \n

#     """
#     # crear la respuesta para que el sistema sepa que es un pdf
#     response = HttpResponse(content_type='application/pdf')

#     # esto para que el archivo sea directamente descargado desde el navegador 
#     response['Content-Disposition'] = f'attachment; filename= Reporte_ZenUN_{nombreArchivoReporte}.pdf'

#     # Crear el Objeto PDF, usando BytesIO; buffer espacio temporal de memoria fisica
#     buffer = BytesIO()
#     lienzo = canvas.Canvas(buffer, pagesize=A4) # pagesize = (21cm, 29.7cm) or (595, 842)

#     ## INICIO Contenido pdf con reportlab

#     if numeroReporte == 1:
#         # obtener lo que se paso como mensajes por la url 
#         fechaInicio = request.GET.get('fechaInicio')
#         fechaFin = request.GET.get('fechaFin')
#         nombreImplemento = request.GET.get('nombreImplemento') 
#         generarCanvas_Reporte_prestamo(lienzo, fechaInicio, fechaFin, nombreImplemento)  

#     elif numeroReporte ==2:
#         # obtener lo que se paso como mensajes por la url 
#         fechaInicio = request.GET.get('fechaInicio')
#         fechaFin = request.GET.get('fechaFin')
#         lugarEvento = request.GET.get('lugarEvento')
#         opciones_seleccionadas = request.GET.get("opciones_seleccionadas")
#         # print(f"\n\n{fechaInicio}\n")
#         generarCanvas_Reporte_Eventos(lienzo, fechaInicio, fechaFin, lugarEvento, opciones_seleccionadas)

#     elif numeroReporte ==3:
#         # obtener lo que se paso como mensajes por la url 
#         idEvento = request.GET.get('idEvento')
#         print(idEvento)
#         #lugarEvento = request.POST.get('lugarEvento')
#         #nombreEvento = request.POST.get('nombreEvento')
#         generarCanvas_Reporte_Asistencia(lienzo, idEvento)

#     else:
#         buffer.close() # Cerrar buffer
#         mensaje = f"El numero de reporte no es correcto, es 1, 2 o 3" 
#         return redirect(reverse("mostrar_vista_informes")+ f'?mensaje={mensaje}')  
        

#     ## FIN de de contenido pdf con reportlab

#     # guardar pdf
#     lienzo.save()
#     # obtener el valor de BytesIO y escribirlo en la respuestaHttp
#     pdf = buffer.getvalue()
#     buffer.close()
#     response.write(pdf)
#     return(response)


# #----------------------- CREAR los REPORTES con reportlab ------------------------------------------
# # Reporte prestamo 
# def generarCanvas_Reporte_prestamo(lienzo:canvas.Canvas, id:str):
#     ##----------------HEADER ---------------------------------
#         #header-titulo
#     lienzo.setLineWidth(.3)
#     lienzo.setFont('Helvetica', 22)
#             # X desde el lad IZQ cuanto mover a la DER
#             # y desde al lad ABJ cuanto mover ARRIBA
#         # header-subtitulo
#     lienzo.drawString(x=30, y=750,text='ZenUN')
#     lienzo.setFont('Helvetica', 12)


#     lienzo.drawString(30, 730, "Reporte PRESTAMOS")
#         # header-hora
#     hora_inicio_reserva = djangoTimeZone.now() + timedelta(hours=-5)
#     fecha_formateada = hora_inicio_reserva.strftime('%Y-%m-%d %H:%M:%S') # Formatear la fecha y hora

#     lienzo.setFont("Helvetica-Bold", 12)
#     lienzo.drawString(350, 750, f"Fecha Reporte: {fecha_formateada}")
    
#     ## --------------ARRAY DE DATOS PARA LAS TABLAS ----------------
#     data = []   # Datos de la tabla se pasan mediante un array de arrays 

#     ## ------------------ MODIFICAR OBJETOS FECHA -------------------
#     # print(f"{fechaInicio}, {fechaFin}")
#     # objeto_fechaInicio = datetime.strptime(fechaInicio, '%Y-%m-%d')   # Asi se crea un obj. datetime  pero sin zona horaria
    
#     objeto_fechaInicio = datetime.strptime(fechaInicio, '%Y-%m-%d').replace(tzinfo=datetimeTimeZone.utc)                                            # pero la BD los objetos fecha tienen zona horario
#     objeto_fechaFinal = (datetime.strptime(fechaFin, '%Y-%m-%d')  + timedelta(days=1) - timedelta(seconds=1)).replace(tzinfo=datetimeTimeZone.utc)  # para que quede en 23:59:59 de ese dia

#     ## ------------------- PRIMERA TABLA------------------------------
    
#     # SACAR DATOS BD 
#     BDDatos = []                                                                                                          # es un array para guardar el contenido de la tabla sin estilo 
#     prestamos_implemento = prestamo.objects.select_related('idImplemento', "estadoPrestamo", "estudianteNumeroDocumento") # consulta
    
#     if nombreImplemento != "":
#         for nuevaTabla in prestamos_implemento:
#             # Ingresar los datos que cumplan los filtros NombreImp. y fechas
#             if((nuevaTabla.idImplemento.nombreImplemento == nombreImplemento) and (objeto_fechaInicio <= nuevaTabla.fechaHoraCreacion <= objeto_fechaFinal)):
#                 row = [ 
#                     nuevaTabla.idPrestamo,                                    #idPrestamo
#                     nuevaTabla.estudianteNumeroDocumento.correoInstitucional, #estudianteCorreo
#                     nuevaTabla.idImplemento.nombreImplemento,                 # nombreImplemento
#                     nuevaTabla.fechaHoraCreacion,                             #fechaInicioPrestamo
#                     nuevaTabla.estadoPrestamo.nombreEstado                    #estadoPrestamo
#                 ]
#                 BDDatos.append(row)
#             else:
#                 pass
#     else:
#         for nuevaTabla in prestamos_implemento:
#             # Ingresar los datos que cumplan el filtro de fecha 
#             if((objeto_fechaInicio <= nuevaTabla.fechaHoraCreacion <= objeto_fechaFinal)):
#                 row = [ 
#                     nuevaTabla.idPrestamo,                                    #idPrestamo
#                     nuevaTabla.estudianteNumeroDocumento.correoInstitucional, #estudianteCorreo
#                     nuevaTabla.idImplemento.nombreImplemento,                 #nombreImplemento
#                     nuevaTabla.fechaHoraCreacion,                             #fechaInicioPrestamo
#                     nuevaTabla.estadoPrestamo.nombreEstado                    #estadoPrestamo
#                 ]
#                 BDDatos.append(row)
#             else:
#                 pass

    
#     #----- CREACION ESTILOS---------
#     # Llamar a los Estilos
#     styles = getSampleStyleSheet() # nos da una lista de estilos a escoger de la biblioteca
    
#     # Creacion estilo <-- header tabla
#     styleHeaderTable = ParagraphStyle('styleHeaderTable',  
#         parent= styles['Heading1'],
#         fontSize=10, 
#         alignment=1  # Center alignment
#     )

#     # Creacion estilo <-- contenido tabla   
#     styleN = ParagraphStyle('p',  
#         parent=styles["BodyText"],
#         fontSize=7, 
#         alignment=1  # Center alignment
#     )


#     # Títulos de las columnas (primera fila)
#     # Paragraph <-- le da estilo a un texto 
#     #                       texto           , estilo 
#     idPrestamo      = Paragraph('idPrestamo', styleHeaderTable)
#     alumnoCorreo    = Paragraph('alumnoCorreo', styleHeaderTable)
#     nombreImplemento= Paragraph('nombreImplemento', styleHeaderTable)
#     fechaPrestamo   = Paragraph('fechaPrestamo inicio', styleHeaderTable)
#     estadoPrestamo  = Paragraph('estadoPrestamo', styleHeaderTable)

#     # Pasar datos al (array data)
#     data.append([idPrestamo, alumnoCorreo, nombreImplemento, fechaPrestamo, estadoPrestamo])


#     # Variable HIGH para saber cuanto mover la tabla relativamente hacia arriba 
#     high = 700

#     # ¿Cuantos prestamos se hicieron en la consulta?
#     prestamoTotalConsultaBD1 = len(BDDatos)


#     # Agregar (datos BD) al (array data)
#     for datoBd in BDDatos:
#         row = []
#         for item in datoBd:
#             # Poner estilo a ese dato
#             dato = Paragraph(str(item), styleN)
#             row.append(dato)

#         high -= 18
#         data.append(row)

#         # CAMBIAR PAGINA, si se pasa de un numero de datos o high especifico 
#         if high < 360:
#             # Poner tabla en el CANVAS
#             crearTablaReportLab(data, lienzo, 5, valorHigh= 700, PonerDesdeLimiteAbajo = True, alturaRow= 18, anchoCol= 3.7)

#             # Cambiar el high a 750, ya que alcanzo limite pagina 
#             high = 750
            
#             # Limpiar datos del array de datos de la tabla 
#             data.clear() 

#             # Agregar los (nombres Columnas) a la tabla otra vez 
#             data.append([idPrestamo, alumnoCorreo, nombreImplemento, fechaPrestamo, estadoPrestamo])

#     # PARA LOS DATOS RESTANTES, si falto dibujar una parte de la tabla
#     crearTablaReportLab(data, lienzo, 5, valorHigh=600, PonerDesdeLimiteAbajo = False, alturaRow= 20, anchoCol= 3.7)

#     ##------------------ CUANTOS PRESTAMOS ----------------------------------
#     lienzo.setFont('Helvetica', 10)
#     lienzo.drawString(x=30, y=750,text=f'''1.5  ¡TOTAL PRESTAMOS, CON FILTROS!, ¿Cuántos prestamos hay?:''')
#     lienzo.setFont('Helvetica-Bold', 15)
#     lienzo.drawString(x=370, y=750,text=f'''{prestamoTotalConsultaBD1} ''')
#     lienzo.setFont('Helvetica', 10)
#     lienzo.drawString(x=30, y=735,text='---------------------------------------------------------------------------------------------------------------------------')

#     ##------------------ SEGUNDA TABLA ----------------------------------
#     lienzo.drawString(x=30, y=720,text='2. ¡TOTAL, SIN FILTROS!, ¿Cuántas veces fueron prestados cada implemento TABLA?:')
#     lienzo.setFont('Helvetica', 10)

#     # resetear array de data
#     data = []

#     # resetar array
#     BDDatos = []
#     numeroTotalPrestamos = 0

#     # CONSULTA  2 BD 
#     resultadoTabla = prestamo.objects.values('idImplemento__nombreImplemento').annotate(contadorPrestamo=Count('idPrestamo')).order_by('idImplemento__nombreImplemento')
    
#     for filaResultado in resultadoTabla:
#         row = [ 
#             filaResultado['idImplemento__nombreImplemento'],
#             filaResultado['contadorPrestamo']
#         ]
#         numeroTotalPrestamos += filaResultado['contadorPrestamo']
#         BDDatos.append(row)
#         # print(row)

#     # Títulos de las columnas (primera fila); los estilos ya estan creados entonces solo colocar la tabla
#     nombreImplemento   = Paragraph('nombreImplemento', styleHeaderTable)
#     contadorPrestamo   = Paragraph('contadorPrestamo', styleHeaderTable)

#     # Pasar datos al (array data)
#     data.append([nombreImplemento, contadorPrestamo])

#     # poner un nuevo HIGH 
#     high = 750
#     numeroDatosContenidoRecorrido = 0

#     # Agregar (datos BD) al (array data)
#     for datoBd in BDDatos:
#         row = []
#         for item in datoBd:
#             # Poner stilo al dato 
#             dato = Paragraph(str(item), styleN)
#             row.append(dato)

#         high -= 12 # mas corto por que la altura de las filas es mas corta
#         data.append(row)
#         numeroDatosContenidoRecorrido += 1

#         # PARA CAMBIAR DE PÁGINA SI YA HAY MUCHOS ELEMENTOS 
#         if high < 360:
#             # Poner tabla en el CANVAS
#             crearTablaReportLab(data, lienzo, 2, valorHigh=650, PonerDesdeLimiteAbajo=False, alturaRow= 18, anchoCol= 6.5)

#             # cambiar el high a 750, ya que alcanzo limite pagina 
#             high = 750

#             # resetear el (array data)
#             data.clear()

#             # agregar el header a la tabla otra vez 
#             data.append([nombreImplemento, contadorPrestamo])

#     # PARA LOS DATOS RESTANTES, si falto dibujar una parte de la tabla
#     crearTablaReportLab(data, lienzo, 2, valorHigh=650,PonerDesdeLimiteAbajo=False, alturaRow= 15, anchoCol= 6.5)

#     ##---------------------- NUMERO TOTAL DE TABLA 2  -------------------------------------
#     lienzo.setLineWidth(.3)
#     lienzo.drawString(x=30, y=750,text=f'3.  ¡TOTAL, SIN FILTROS!, ¿Cuántas veces fueron prestados los implemento VALOR?: ')
#     lienzo.setFont('Helvetica-Bold', 15)
#     lienzo.drawString(x=500, y=750,text=f'''{numeroTotalPrestamos} ''')
#     #Trazabilidad informe de préstamos, idInforme 3
#     tipo_informe = tipoInforme.objects.get(pk=3)
#     nuevo_informe = trazabilidadInformes(
#         fechaGeneracionInforme = fecha_formateada,
#         tipoInforme = tipo_informe
#     )
#     nuevo_informe.save()
#     return None


# def crearTablaReportLab(data, lienzo:canvas.Canvas, numeroColumnas:int, valorHigh=650, PonerDesdeLimiteAbajo=True, alturaRow=18, anchoCol=3.7 ):
#     """_summary_Este metodo es para crear una tabla pasando unos datos y si necesita pasar de pagina en el PDF \n

#     Args:\n
#         \n\t\t data (array): Array de arrays: cada sub array es una fila 
#         \n\t\t lienzo (canvas.Canvas): lienzo canvas
#         \n\t\t numeroColumnas (int): numero de columnas de la tabla
#         \n\t\t valorHigh (int, optional): valor para desde abajo subir la tabla. Defaults to 650.
#         \n\t\t PonerDesdeLimiteAbajo (bool, optional): se pone en 100 la altura de la tabla desde abajo. Defaults to True.
#         \n\t\t alturaRow (int, optional): altura de la fila. Defaults to 18.
#         \n\t\t anchoCol (float, optional): El ancho de la columna. Defaults to 3.7.\n
       
#     """
#     high = valorHigh - (len(data) * alturaRow)

#     # crear la tabla  y estilizar la tabla
#     anchoColumnas = [anchoCol * cm] * numeroColumnas
#     table = Table(data, colWidths=anchoColumnas)
#     table.setStyle(TableStyle([
#         ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
#         ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
#         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#         ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
#     ]))
#     # Tamaño del PDF
#     ancho, alto = A4

#     # Ajuste de coordenadas para evitar que la tabla se dibuje fuera de los márgenes
#     table.wrapOn(lienzo, ancho, alto)
#     if(PonerDesdeLimiteAbajo):
#         table.drawOn(lienzo, 30, 100) 
#     else:
#         table.drawOn(lienzo, 30, high) 
    
#     # Cambiar de página si es necesario
#     lienzo.showPage()
#     return(None)

