import sqlite3
import os
from datetime import datetime, timedelta

def init_db():
    """
    Inicializa la base de datos creando las tablas necesarias
    y añadiendo datos iniciales si no existen.
    """
    if not os.path.exists("data"):
        os.makedirs("data")
        
    conn = sqlite3.connect("data/citas.db")
    cursor = conn.cursor()
    
    # Crear tabla de doctores
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS doctores (
        id INTEGER PRIMARY KEY,
        nombre TEXT NOT NULL,
        especialidad TEXT NOT NULL,
        disponible BOOLEAN NOT NULL DEFAULT 1
    )
    ''')
    
    # Crear tabla de horarios
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS horarios (
        id INTEGER PRIMARY KEY,
        doctor_id INTEGER NOT NULL,
        fecha TEXT NOT NULL,
        hora_inicio TEXT NOT NULL,
        hora_fin TEXT NOT NULL,
        disponible BOOLEAN NOT NULL DEFAULT 1,
        FOREIGN KEY (doctor_id) REFERENCES doctores (id)
    )
    ''')
    
    # Crear tabla de citas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS citas (
        id INTEGER PRIMARY KEY,
        paciente_id TEXT NOT NULL,
        doctor_id INTEGER NOT NULL,
        fecha TEXT NOT NULL,
        hora TEXT NOT NULL,
        motivo TEXT NOT NULL,
        estado TEXT NOT NULL DEFAULT 'AGENDADA',
        FOREIGN KEY (doctor_id) REFERENCES doctores (id)
    )
    ''')
    
    # Insertar datos de prueba si no existen
    cursor.execute("SELECT COUNT(*) FROM doctores")
    if cursor.fetchone()[0] == 0:
        # Insertar doctores de ejemplo
        doctores = [
            (1, "Dr. Carlos Mendoza", "Medicina General", 1),
            (2, "Dra. María López", "Cardiología", 1),
            (3, "Dr. Juan Pérez", "Pediatría", 1),
            (4, "Dra. Ana García", "Dermatología", 1)
        ]
        cursor.executemany("INSERT INTO doctores VALUES (?, ?, ?, ?)", doctores)
        
        # Generar horarios para los próximos 30 días
        horarios = []
        horario_id = 1
        for doctor_id in range(1, 5):
            for day in range(30):
                fecha = (datetime.now() + timedelta(days=day)).strftime("%Y-%m-%d")
                # No generar horarios para fin de semana
                weekday = (datetime.now() + timedelta(days=day)).weekday()
                if weekday < 5:  # Lunes a Viernes
                    horarios.append((horario_id, doctor_id, fecha, "08:00", "09:00", 1))
                    horario_id += 1
                    horarios.append((horario_id, doctor_id, fecha, "09:00", "10:00", 1))
                    horario_id += 1
                    horarios.append((horario_id, doctor_id, fecha, "10:00", "11:00", 1))
                    horario_id += 1
                    horarios.append((horario_id, doctor_id, fecha, "11:00", "12:00", 1))
                    horario_id += 1
                    horarios.append((horario_id, doctor_id, fecha, "14:00", "15:00", 1))
                    horario_id += 1
                    horarios.append((horario_id, doctor_id, fecha, "15:00", "16:00", 1))
                    horario_id += 1
                    horarios.append((horario_id, doctor_id, fecha, "16:00", "17:00", 1))
                    horario_id += 1
        
        cursor.executemany("INSERT INTO horarios VALUES (?, ?, ?, ?, ?, ?)", horarios)
    
    conn.commit()
    conn.close()