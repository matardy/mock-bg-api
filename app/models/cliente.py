from pydantic import BaseModel
from typing import Optional

class Cliente(BaseModel):
    id: int
    identificacion: str
    tipoIdentificacion: str
    nombres: str
    direccion1: str
    telefono1: int
    correoElectronico: str
    telefonoCelular: str
    segmentoEstrategico: str
    calificacion: str
    estado: str
    sexo: str
    fechaNacimiento: str
    oficial: str
    clienteDesde: str
    clave_cajero: Optional[str] = None

class Autenticacion(BaseModel):
    identificacion: str
    clave_cajero: str