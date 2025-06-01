from pydantic import BaseModel, Field # esta librería permite definir modelos de datos y validarlos automáticamente

# OJO NO NECESITA CONSTRUCTOR, Pydantic maneja la creación de instancias automáticamente
class form_pre_registro(BaseModel):
    apellidos: str
    nombres: str
    tipoDocumento: str
    numeroDocumento: str
    fechaNacimiento: str
    paisNacimiento: str
    departamentoNacimiento: str
    municipioNacimiento: str
    categoriaSisben: str
    subcategoriaSisben: str
    direccionResidencia: str
    telefono: str
    rutaEscolar: str
    seguroMedico: str
    discapacidad: str
    detalleDiscapacidad: str
    poblacionDesplazada: str
    fechaDesplazamiento: str
    paisResidencia: str
    departamentoResidencia: str
    municipioResidencia: str
    gradoIngreso: str
    institucionAnterior: str
    municipioAnterior: str
    sede: str
    acudiente1Parentesco: str
    acudiente1Apellidos: str
    acudiente1Nombres: str
    acudiente1CC: str
    acudiente1Celular: str
    acudiente1Ocupacion: str
    acudiente2Parentesco: str
    acudiente2Apellidos: str
    acudiente2Nombres: str
    acudiente2CC: str
    acudiente2Celular: str
    acudiente2Ocupacion: str



# // Tipado del formulario
# type FormData = {
#   apellidos: string;
#   nombres: string;
#   tipoDocumento: string;
#   numeroDocumento: string;
#   fechaNacimiento: string;
#   paisNacimiento: string;
#   departamentoNacimiento: string;
#   municipioNacimiento: string;
#   categoriaSisben: string;
#   subcategoriaSisben: string;
#   direccionResidencia: string;
#   telefono: string;
#   rutaEscolar: string;
#   seguroMedico: string;
#   discapacidad: string;
#   detalleDiscapacidad: string;
#   poblacionDesplazada: string;
#   fechaDesplazamiento: string;
#   paisResidencia: string;
#   departamentoResidencia: string;
#   municipioResidencia: string;
#   gradoIngreso: string;
#   institucionAnterior: string;
#   municipioAnterior: string;
#   sede: string;
#   acudiente1Parentesco: string;
#   acudiente1Apellidos: string;
#   acudiente1Nombres: string;
#   acudiente1CC: string;
#   acudiente1Celular: string;
#   acudiente1Ocupacion: string;
#   acudiente2Parentesco: string;
#   acudiente2Apellidos: string;
#   acudiente2Nombres: string;
#   acudiente2CC: string;
#   acudiente2Celular: string;
#   acudiente2Ocupacion: string;
# };