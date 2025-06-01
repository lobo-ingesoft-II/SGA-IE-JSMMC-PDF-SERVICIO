from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT  


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
