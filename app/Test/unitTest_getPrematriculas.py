import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from app.services.prematricula_service import obtener_prematriculas  # Cambia esto por la ruta real


@patch("app.services.prematricula_service.requests.get") # Esta línea reemplaza temporalmente la función requests.get() dentro del módulo
def test_obtener_prematriculas_success(mock_get):
    # Simular respuesta HTTP exitosa con JSON
    mock_response = MagicMock() # Simular respuesta HTTP exitosa con JSON
    mock_response.status_code = 200 
    mock_response.json.return_value = {"documento": {"nombre": "Juan"}} # efine que si se llama a .json() sobre la respuesta, devolverá este diccionario
    mock_get.return_value = mock_response # Le dice al mock de requests.get() que, cuando sea llamado, devuelva mock_response.

    result = obtener_prematriculas("123456")

    assert result == {"nombre": "Juan"}

@patch("app.services.prematricula_service.requests.get")
def test_obtener_prematriculas_empty(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    mock_get.return_value = mock_response

    result = obtener_prematriculas("123456")
    assert result is None


@patch("app.services.prematricula_service.requests.get")
def test_obtener_prematriculas_error_status(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    result = obtener_prematriculas("123456")
    assert result is None
