import sqlite3
import os
from sqlite3 import Connection, Cursor, Row

def get_db_connection() -> Connection:
    """
    Crea y retorna una conexión a la base de datos SQLite.
    Configura row_factory para que los resultados sean accesibles como diccionarios.
    """
    if not os.path.exists("data"):
        os.makedirs("data")
        
    conn = sqlite3.connect("data/citas.db")
    conn.row_factory = sqlite3.Row
    return conn