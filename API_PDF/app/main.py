from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import pdf_pre_registro_route  # Importar las rutas del módulo pdf_pre_registro


# Instancia de FastAPI
app = FastAPI()

# Importar las rutas
app.include_router(pdf_pre_registro_route.router)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todas las orígenes
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos HTTP
    allow_headers=["*"],  # Permitir todos los encabezados
)

# if __name__ == '__main__':
#     app.run(debug=True)