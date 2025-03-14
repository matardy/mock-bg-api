from pydantic import BaseModel
from typing import Optional

class Cita(BaseModel):
    id: Optional[int] = None
    paciente_id: str  # identificacion del cliente
    doctor_id: int
    fecha: str
    hora: str
    motivo: str
    estado: str = "AGENDADA"  # AGENDADA, CANCELADA, COMPLETADA
    
class CitaResponse(BaseModel):
    id: int
    paciente: str  # nombre del paciente
    doctor: str    # nombre del doctor
    especialidad: str
    fecha: str
    hora: str
    motivo: str
    estado: str