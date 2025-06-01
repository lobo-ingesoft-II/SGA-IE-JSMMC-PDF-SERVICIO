import requests # Para hacer solicitudes HTTP 
from app.backend.config import settings

# FUNCIÓN PARA OBTENER JSON DESDE LA API(PRE-MATRICULA)
async def obtener_prematriculas(id: str):
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