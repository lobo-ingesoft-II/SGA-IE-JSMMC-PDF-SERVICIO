from fastapi import APIRouter # para crear rutas en FastAPI modulares
from fastapi import HTTPException # para manejar excepciones HTTP
from bson import ObjectId # para manejar ObjectId de MongoDB
from app.services.generacion_pdf_pre_registro import obtener_prematriculas # Importar el servicio de generación de PDF


from app.backend.session import db # Importar la base de datos desde el archivo de sesión
from app.schemas.form_pre_registro import form_pre_registro # Importar el modelo de datos para validación

router = APIRouter() # Crear una instancia del enrutador


# Ruta para generar un PDF de pre-registro 
@router.post("/pdf_pre_registro/{id}")
def generate_pdf_pre_registro(id: str):

    print(f"Iniciaando el proceso de generación PDF de pre-registro para el ID: {id}")

    # Obtener el JSON del pre-registro desde la base de datos 
    response = obtener_prematriculas(id)

    # Si la respuesta es None, lanzar una excepción HTTP 404 
    if not response:
        raise HTTPException(status_code=404, detail="No se encontraron datos para generar el PDF, id no válido o no existe.")
    
    return response  # Retornar la respuesta del servicio de generación de PDF