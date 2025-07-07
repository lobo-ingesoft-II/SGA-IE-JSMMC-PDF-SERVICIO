from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.routers import pdf_pre_registro_route  # Importar las rutas del módulo pdf_pre_registro

# Librerias para Observabilidad
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time
from starlette.responses import Response
from app.routers.pdf_pre_registro_route import REQUEST_COUNT_PDF_PRE_REGISTRATION_ROUTERS, REQUEST_LATENCY_PDF_PRE_REGISTRATION_ROUTERS, ERROR_COUNT_PDF_PRE_REGISTRATION_ROUTERS



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

# Middleware para observabilidad
@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    try:
        response = await call_next(request)
        status = response.status_code
    except Exception as e:
        status = 500
        raise e
    finally:
        latency = time.time() - start_time
        endpoint = request.url.path
        method = request.method

        REQUEST_COUNT_PDF_PRE_REGISTRATION_ROUTERS.labels(endpoint=endpoint, method=method).inc()
        REQUEST_LATENCY_PDF_PRE_REGISTRATION_ROUTERS.labels(endpoint=endpoint, method=method).observe(latency)


        
        if status >= 400:
            ERROR_COUNT_PDF_PRE_REGISTRATION_ROUTERS.labels(endpoint=endpoint, method=method, status_code=str(status)).inc()

    return response
# if __name__ == '__main__':
#     app.run(debug=True)