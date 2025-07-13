# Changelog
---

## [1.6.0]

### Added
- Implementación de pruebas unitarias para los servicios de MongoDB.
- Política de ramas Git (`gitflow-branch-policy.yml`).
- Métricas de observabilidad con Prometheus (`prometheus-client`).
- Pruebas para generación de PDF con ReportLab.
- Función `descarga_reportes()` para exportar PDF.
- Mocking de `requests.get` para pruebas HTTP.
- Parcheo de dependencias y testeo con `pytest`.

### Changed
- Refactor en rutas y organización de carpetas dentro de `services/`.
- Mejoras de estilo y organización en la generación de PDF.
- Actualización de `README.md` con instrucciones y dependencias.
- Actualización de `requirements.txt` para incluir paquetes de métricas.

---

## [1.5.0] - 2025-07-13

### Added
- Pruebas unitarias automatizadas con `pytest`.
- Generación de reporte de estudiante en formato PDF.
- Configuración inicial de monitoreo con Prometheus.

### Changed
- Refactorización de rutas (`routes`) para mejor organización.
- Mejora en la documentación (`README.md`).

---

## [1.4.0] - 2025-07-10

### Added
- Política de ramas Git (`gitflow-branch-policy.yml`).

---

## [1.3.0] - 2025-07-06

### Added
- Integración de Prometheus para métricas de observabilidad.
- Actualización del archivo `requirements.txt` con nuevas dependencias.

---

## [1.2.0] - 2025-06-07

### Added
- Escudo institucional en el encabezado del PDF.
- Segunda tabla con datos académicos del estudiante.
- Tercera y cuarta tablas con información de acudientes.

---

## [1.1.0] - 2025-06-01

### Added
- Funcionalidad básica del sistema de PDF terminada.
- Rutas `GET`, `POST`, `PUT`, `DELETE` operativas para prematrícula.
- JSON de prueba para pre-matrícula funcional.

### Changed
- Reorganización de carpetas y módulos en `services/`.
- Refactor de funciones para reutilización y mantenibilidad.

---

## [1.0.0] - 2025-05-31

### Added
- Estructura base del proyecto.
- Primer archivo `README.md`.
- Primer commit del backend con FastAPI.
