from fastapi import APIRouter # para crear rutas en FastAPI modulares
from fastapi import HTTPException # para manejar excepciones HTTP
from fastapi.responses import StreamingResponse # para enviar respuestas de flujo de datos
from fastapi import BackgroundTasks # para manejar dependencias en FastAPI
from bson import ObjectId # para manejar ObjectId de MongoDB
from app.services.prematricula_service import obtener_prematriculas # Importar el servicio de generación de PDF


from app.backend.session import db # Importar la base de datos desde el archivo de sesión
from app.schemas.form_pre_registro import form_pre_registro # Importar el modelo de datos para validación
from app.services.generacion_pdf_pre_registro_service import descarga_reportes  # Importar el servicio de generación de PDF

router = APIRouter() # Crear una instancia del enrutador


# Ruta para generar un PDF de pre-registro 
@router.post(
    "/pdf_pre_registro/{id}",
    summary="Generar y descargar PDF de pre-registro",
    response_description="Archivo PDF generado con la información del pre-registro",
    responses={
        200: {
            "content": {"application/pdf": {}},
            "description": "PDF generado exitosamente"
        },
        404: {
            "description": "No se encontraron datos para generar el PDF, id no válido o no existe."
        }
    },
)
async def generate_pdf_pre_registro(id: str, background_tasks: BackgroundTasks):
    """
    Genera y descarga el PDF de pre-registro de un estudiante.

    Este endpoint obtiene la información de pre-registro del estudiante con el ID proporcionado,
    valida los datos y genera un archivo PDF con la información correspondiente. El PDF se descarga
    automáticamente en el navegador del usuario.

    **Parámetros:**
    - **id** (`str`): ID del pre-registro del estudiante.

    **Respuestas:**
    - **200**: Retorna el archivo PDF generado.
    - **404**: No se encontraron datos para el ID proporcionado.

    **Ejemplo de uso:**
    ```
    POST /pdf_pre_registro/6838ab661efa82c1dca6d3ed
    ```
    """
    print(f"Iniciaando el proceso de generación PDF de pre-registro para el ID: {id}")

    # Obtener el JSON del pre-registro desde la base de datos 
    JSON_response = await obtener_prematriculas(id)

    # Si la respuesta es None, lanzar una excepción HTTP 404 
    if not JSON_response:
        raise HTTPException(status_code=404, detail="No se encontraron datos para generar el PDF, id no válido o no existe.")
    
    # Validar el JSON obtenido contra el modelo form_pre_registro
    JSON_response = form_pre_registro.model_validate(JSON_response)

    # convertir a un diccionario para poder imprimirlo
    DIC_response = JSON_response.model_dump()

    ## LLAMAR AL SERVICIO DE GENERACIÓN DE PDF
    buffer = await descarga_reportes(DIC_response)

    # print(f"Datos obtenidos del pre-registro: {DIC_response}")

    headers = {
        "Content-Disposition": f"attachment; filename=pre_registro_{id}.pdf",
        "Content-Type": "application/pdf",
    }

    return StreamingResponse(buffer, media_type="application/pdf", headers=headers)  # Retornar la respuesta del servicio de generación de PDF