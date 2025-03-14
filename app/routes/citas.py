from fastapi import APIRouter, HTTPException
from typing import List
from ..models.cita import Cita, CitaResponse
from ..models.doctor import DisponibilidadFilter
from ..db.database import get_db_connection
import json

router = APIRouter()

def load_clientes():
    with open("data/clientes.json", "r") as file:
        return json.load(file)["data"]

@router.post("/disponibilidad")
async def consultar_disponibilidad(filtros: DisponibilidadFilter = None):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """
    SELECT h.id, d.id as doctor_id, d.nombre as doctor, d.especialidad, h.fecha, h.hora_inicio, h.hora_fin
    FROM horarios h
    JOIN doctores d ON h.doctor_id = d.id
    WHERE h.disponible = 1 AND d.disponible = 1
    """
    params = []
    
    if filtros:
        if filtros.especialidad:
            query += " AND d.especialidad = ?"
            params.append(filtros.especialidad)
        if filtros.fecha:
            query += " AND h.fecha = ?"
            params.append(filtros.fecha)
        if filtros.doctor_id:
            query += " AND d.id = ?"
            params.append(filtros.doctor_id)
    
    query += " ORDER BY h.fecha, h.hora_inicio"
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    
    disponibilidad = []
    for row in rows:
        disponibilidad.append({
            "horario_id": row["id"],
            "doctor_id": row["doctor_id"],
            "doctor": row["doctor"],
            "especialidad": row["especialidad"],
            "fecha": row["fecha"],
            "hora_inicio": row["hora_inicio"],
            "hora_fin": row["hora_fin"]
        })
    
    return disponibilidad

@router.post("/citas")
async def agendar_cita(cita: Cita):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Verificar si el horario está disponible
    cursor.execute(
        """
        SELECT COUNT(*) FROM horarios 
        WHERE doctor_id = ? AND fecha = ? AND hora_inicio = ? AND disponible = 1
        """, 
        (cita.doctor_id, cita.fecha, cita.hora)
    )
    
    if cursor.fetchone()[0] == 0:
        conn.close()
        raise HTTPException(status_code=400, detail="El horario seleccionado no está disponible")
    
    # Verificar si el paciente existe
    clientes = load_clientes()
    paciente_existe = False
    for cliente in clientes:
        if cliente["identificacion"] == cita.paciente_id:
            paciente_existe = True
            break
    
    if not paciente_existe:
        conn.close()
        raise HTTPException(status_code=400, detail="El paciente no existe")
    
    # Insertar la cita
    cursor.execute(
        """
        INSERT INTO citas (paciente_id, doctor_id, fecha, hora, motivo, estado)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (cita.paciente_id, cita.doctor_id, cita.fecha, cita.hora, cita.motivo, cita.estado)
    )
    
    # Actualizar disponibilidad del horario
    cursor.execute(
        """
        UPDATE horarios SET disponible = 0
        WHERE doctor_id = ? AND fecha = ? AND hora_inicio = ?
        """,
        (cita.doctor_id, cita.fecha, cita.hora)
    )
    
    conn.commit()
    
    # Obtener el ID de la cita creada
    cita_id = cursor.lastrowid
    
    conn.close()
    
    return {"id": cita_id, **cita.dict(), "message": "Cita agendada con éxito"}

@router.put("/citas/{cita_id}/cancelar")
async def cancelar_cita(cita_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Verificar si la cita existe
    cursor.execute("SELECT * FROM citas WHERE id = ?", (cita_id,))
    cita = cursor.fetchone()
    
    if not cita:
        conn.close()
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    
    if cita["estado"] == "CANCELADA":
        conn.close()
        raise HTTPException(status_code=400, detail="La cita ya está cancelada")
    
    # Actualizar estado de la cita
    cursor.execute(
        "UPDATE citas SET estado = 'CANCELADA' WHERE id = ?",
        (cita_id,)
    )
    
    # Liberar el horario
    cursor.execute(
        """
        UPDATE horarios SET disponible = 1
        WHERE doctor_id = ? AND fecha = ? AND hora_inicio = ?
        """,
        (cita["doctor_id"], cita["fecha"], cita["hora"])
    )
    
    conn.commit()
    conn.close()
    
    return {"message": "Cita cancelada con éxito"}

@router.get("/citas/paciente/{identificacion}")
async def consultar_citas_paciente(identificacion: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Consultar citas del paciente
    cursor.execute(
        """
        SELECT c.id, c.paciente_id, c.doctor_id, 
               d.nombre as doctor, d.especialidad, c.fecha, c.hora, c.motivo, c.estado
        FROM citas c
        JOIN doctores d ON c.doctor_id = d.id
        WHERE c.paciente_id = ?
        ORDER BY c.fecha DESC, c.hora DESC
        """,
        (identificacion,)
    )
    
    rows = cursor.fetchall()
    conn.close()
    
    # Obtener nombres de pacientes
    clientes = load_clientes()
    cliente_dict = {}
    for cliente in clientes:
        cliente_dict[cliente["identificacion"]] = cliente["nombres"]
    
    citas = []
    for row in rows:
        row_dict = dict(row)
        citas.append({
            "id": row["id"],
            "paciente": cliente_dict.get(row["paciente_id"], "Desconocido"),
            "doctor": row["doctor"],
            "especialidad": row["especialidad"],
            "fecha": row["fecha"],
            "hora": row["hora"],
            "motivo": row["motivo"],
            "estado": row["estado"]
        })
    
    return citas

@router.get("/citas/{cita_id}")
async def obtener_cita(cita_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Consultar detalles de la cita
    cursor.execute(
        """
        SELECT c.id, c.paciente_id, c.doctor_id, 
               d.nombre as doctor, d.especialidad, c.fecha, c.hora, c.motivo, c.estado
        FROM citas c
        JOIN doctores d ON c.doctor_id = d.id
        WHERE c.id = ?
        """,
        (cita_id,)
    )
    
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    
    # Obtener nombre del paciente
    clientes = load_clientes()
    paciente_nombre = "Desconocido"
    for cliente in clientes:
        if cliente["identificacion"] == row["paciente_id"]:
            paciente_nombre = cliente["nombres"]
            break
    
    return {
        "id": row["id"],
        "paciente": paciente_nombre,
        "doctor": row["doctor"],
        "especialidad": row["especialidad"],
        "fecha": row["fecha"],
        "hora": row["hora"],
        "motivo": row["motivo"],
        "estado": row["estado"]
    }

@router.get("/doctores")
async def listar_doctores():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM doctores")
    rows = cursor.fetchall()
    conn.close()
    
    doctores = []
    for row in rows:
        row_dict = dict(row)
        doctores.append({
            "id": row["id"],
            "nombre": row["nombre"],
            "especialidad": row["especialidad"],
            "disponible": bool(row["disponible"])
        })
    
    return doctores