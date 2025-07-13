from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
# Configuración de la conexión a MongoDB
from app.backend.config import settings # Traer el valor de configuración de la URI de MongoDB

# Crear cliente MongoDB
client = MongoClient(settings.mongo_uri, server_api=ServerApi('1'))

# Seleccionar la base de datos
db = client["prematricula_db"]   # OJO: remplazar por la bd a utilizar     

# print("Colecciones en la base de datos:", db.list_collection_names())

# Verifica conexión (opcional)
try:
    client.admin.command('ping')
    print("Conexión a MongoDB exitosa.")
except Exception as e:
    print("Error al conectar a MongoDB:", e)