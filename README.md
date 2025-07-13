# 📄 SGA-IE-JSMMC-PDF-SERVICIO

**Autor:** Jhoan Sebastian Franco Ruiz

---
API o servicio para la creación del PDF de pre-matricula 
---

## 📝 Descripción general

Este servicio permite generar y descargar archivos PDF a partir de los datos de pre-matrícula de estudiantes y acudientes de la Institución Educativa Departamental Josué Manrique.  
Recibe datos desde otro servicio, los valida y construye el PDF de manera automática, exponiendo endpoints REST documentados con Swagger/FastAPI.

---

## 🎯 Funcionalidades

- Generación de reportes PDF a partir de datos JSON de pre-matrícula.
- Descarga inmediata del PDF desde el navegador o herramientas como Postman.
- Modularidad para adaptar la generación de PDF a otros tipos de datos.
- Documentación interactiva con Swagger (FastAPI).

---

## 🔧 Endpoints REST

| Método | Endpoint                          | Descripción                                         |
|--------|-----------------------------------|-----------------------------------------------------|
| POST   | `/pdf_pre_registro/{id}`          | Genera y descarga el PDF de pre-registro por ID     |

---

### Ejemplo de uso (POSTMAN)

**POST EXITOSO**
![imagen](/API_PDF/imagenes/POSTMAN-POST1.png)

**POST FALLIDO**
![imagen](/API_PDF/imagenes/POSTMAN-POST2-CASOFALLIDO.png)

---

### 📑 Swagger

La documentación Swagger está disponible en:  
http://localhost:8015/docs

---

### ⚙️ Configuración (IMPORTANTE)

Crea un archivo `.env` en la raíz del proyecto o FEURA  de la carpeta `API_PDF/` con el siguiente contenido:

```
MONGO_URI=mongodb+srv://usuario:contraseña@host.mongodb.net/tu_basededatos?retryWrites=true&w=majority
SERVIDOR_API_PREMATRICULA_URL=http://localhost:8010
```

---

### 🚀 Instalación y Ejecución

Instala las dependencias:
```bash
pip install -r requirements.txt
```

Correr el servidor 

```bash
uvicorn app.main:app --reload --port 8015
```

---
### ¿Porque puerto 8015 para el servidor Uvicorn?
Para no tener interferencias con otras APIS si se corre en local