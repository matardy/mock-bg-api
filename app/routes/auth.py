from fastapi import APIRouter, HTTPException
import json
from ..models.cliente import Autenticacion
from ..db.database import get_db_connection

router = APIRouter()

def load_data(archivo):
    with open(archivo, "r") as file:
        return json.load(file)["data"]

@router.post("/autenticar")
async def autenticar_usuario(autenticacion: Autenticacion):
    clientes = load_data("data/clientes.json")
    for cliente in clientes:
        if cliente["identificacion"] == autenticacion.identificacion and cliente.get("clave_cajero") == autenticacion.clave_cajero:
            return {"autenticado": True}
    return {"autenticado": False}