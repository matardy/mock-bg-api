from pydantic import BaseModel
from typing import Optional

class Doctor(BaseModel):
    id: int
    nombre: str
    especialidad: str
    disponible: bool = True

class Horario(BaseModel):
    id: int
    doctor_id: int
    fecha: str
    hora_inicio: str
    hora_fin: str
    disponible: bool = True

class DisponibilidadFilter(BaseModel):
    especialidad: Optional[str] = None
    fecha: Optional[str] = None
    doctor_id: Optional[int] = None