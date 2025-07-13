import pytest
from io import BytesIO
from unittest.mock import patch, MagicMock

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from app.services.generacion_pdf_pre_registro_service import descarga_reportes

# Diccionario de ejemplo mínimo para el JSON
mock_json = {
    "apellidos": "Franco",
    "nombres": "Juan",
    "tipoDocumento": "Tarjeta de Identidad",
    "numeroDocumento": "123456789",
    "fechaNacimiento": "2010-05-15",
    "paisNacimiento": "COLOMBIA",
    "departamentoNacimiento": "CUNDINAMARCA",
    "municipioNacimiento": "Yopal",
    "categoriaSisben": "A",
    "subcategoriaSisben": "A2",
    "direccionResidencia": "Calle 10 #5-20",
    "telefono": "3201234567",
    "rutaEscolar": "Ruta 1",
    "seguroMedico": "Nueva EPS",
    "discapacidad": "NO",
    "detalleDiscapacidad": "",
    "poblacionDesplazada": "NO",
    "fechaDesplazamiento": "",
    "paisResidencia": "COLOMBIA",
    "departamentoResidencia": "CUNDINAMARCA",
    "municipioResidencia": "Yopal",
    "gradoIngreso": "6",
    "institucionAnterior": "Colegio ABC",
    "municipioAnterior": "Yopal",
    "sede": "INSTITUCIÓN EDUCATIVA DEPARTAMENTAL JOSUÉ MANRIQUE",
    "acudiente1Parentesco": "Padre",
    "acudiente1Apellidos": "Pérez Rodríguez",
    "acudiente1Nombres": "Carlos Alberto",
    "acudiente1CC": "987654321",
    "acudiente1Celular": "3109876543",
    "acudiente1Ocupacion": "Ingeniero",
    "acudiente2Parentesco": "Madre",
    "acudiente2Apellidos": "Gómez Ruiz",
    "acudiente2Nombres": "María Fernanda",
    "acudiente2CC": "1122334455",
    "acudiente2Celular": "3112233445",
    "acudiente2Ocupacion": "Docente"
}

# Esta prueba simula que el lienzo se genera correctamente
@patch("app.services.generacion_pdf_pre_registro_service.generarCanvas_Reporte_prestamo")
@pytest.mark.asyncio
async def test_descarga_reportes_ok(mock_generar_canvas):
    result = await descarga_reportes(mock_json)

    assert isinstance(result, BytesIO)
    assert result.getvalue() != b""  # El buffer no debe estar vacío

    mock_generar_canvas.assert_called_once()
